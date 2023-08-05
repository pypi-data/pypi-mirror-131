import asyncio
import inspect
import logging
import queue
from typing import Any, Union, Type, Dict, TYPE_CHECKING, Optional, Callable, TypeVar, overload, List
import threading

import pyobs.interfaces
from pyobs.events import Event, LogEvent, ModuleClosedEvent
from pyobs.interfaces import Interface
from pyobs.utils.parallel import Future
from .proxy import Proxy
from .commlogging import CommLoggingHandler

if TYPE_CHECKING:
    from pyobs.modules import Module

log = logging.getLogger(__name__)


ProxyType = TypeVar('ProxyType')


class Comm:
    """Base class for all Comm modules in pyobs."""
    __module__ = 'pyobs.comm'

    def __init__(self, cache_proxies: bool = True):
        """Creates a comm module."""

        self._proxies: Dict[str, Proxy] = {}
        self._module: Optional[Module] = None
        self._log_queue: asyncio.Queue[LogEvent] = asyncio.Queue()
        self._cache_proxies = cache_proxies

        # add handler to global logger
        handler = CommLoggingHandler(self)
        handler.setLevel(logging.INFO)
        logging.getLogger().addHandler(handler)

        # logging thread
        self._closing = asyncio.Event()
        self._logging_task: Optional[asyncio.Task] = None

    @property
    def module(self) -> Optional['Module']:
        """The module that this Comm object is attached to."""
        return self._module

    @module.setter
    def module(self, module: 'Module') -> None:
        """The module that this Comm object is attached to."""
        # if we have a _set_module method, call it
        self._set_module(module)

        # store module
        self._module = module

    def _set_module(self, module: 'Module') -> None:
        ...

    async def open(self) -> None:
        """Open module."""

        # start logging thread
        self._logging_task = asyncio.create_task(self._logging())

        # some events
        await self.register_event(ModuleClosedEvent, self._client_disconnected)

    async def close(self) -> None:
        """Close module."""

        # close thread
        self._closing.set()
        if self._logging_task:
            self._logging_task.cancel()

    def _get_full_client_name(self, name: str) -> str:
        """Returns full name for given client.

        Some Comm modules may use short names for their clients. This methods returns the full name
        for a given short name.

        Args:
            name: Short name to get full name for.

        Returns:
            Full name for given client.
        """

        # this base class doesn't have short names
        return name

    async def _get_client(self, client: str) -> Optional[Union['Module', Proxy]]:
        """Get a proxy to the given client.

        Args:
            client: Name of client.

        Returns:
            Proxy class for given client.
        """

        # return module, if "main" is requested
        if client == 'main':
            return self.module
        if client is None:
            return None

        # if client doesn't exist or we disabled caching, fetch a new proxy
        if client not in self._proxies or not self._cache_proxies:
            # get interfaces
            try:
                interfaces = await self.get_interfaces(client)
            except IndexError:
                return None

            # create new proxy
            proxy = Proxy(self, client, interfaces)
            self._proxies[client] = proxy

        # return proxy
        return self._proxies[client]

    @overload
    async def proxy(self, name_or_object: Union[str, object], obj_type: Type[ProxyType]) -> ProxyType:
        ...

    @overload
    async def proxy(self, name_or_object: Union[str, object], obj_type: Optional[Type[ProxyType]] = None) -> Any:
        ...

    async def proxy(self, name_or_object: Union[str, object], obj_type: Optional[Type[ProxyType]] = None) \
            -> Union[Any, ProxyType]:
        """Returns object directly if it is of given type. Otherwise get proxy of client with given name and check type.

        If name_or_object is an object:
            - If it is of type (or derived), return object.
            - Otherwise raise exception.
        If name_name_or_object is string:
            - Create proxy from name and raise exception, if it doesn't exist.
            - Check type and raise exception if wrong.
            - Return object.

        Args:
            name_or_object: Name of object or object itself.
            obj_type: Expected class of object.

        Returns:
            Object or proxy to object.

        Raises:
            ValueError: If proxy does not exist or wrong type.
        """

        if obj_type is not None and isinstance(name_or_object, obj_type):
            # return directly
            return name_or_object

        elif isinstance(name_or_object, str):
            # get proxy
            proxy = await self._get_client(name_or_object)

            # check it
            if proxy is None:
                raise ValueError('Could not create proxy for given name "%s".' % name_or_object)
            elif obj_type is None or isinstance(proxy, obj_type):
                return proxy
            else:
                raise ValueError('Proxy obtained from given name "%s" is not of requested type "%s".' %
                                 (name_or_object, obj_type))

        else:
            # completely wrong...
            raise ValueError('Given parameter is neither a name nor an object of requested type "%s".' % obj_type)

    async def safe_proxy(self, name_or_object: Union[str, object], obj_type: Optional[Type[ProxyType]] = None) \
            -> Optional[Union[Any, ProxyType]]:
        """Calls proxy() in a safe way and returns None instead of raising an exception."""

        try:
            return await self.proxy(name_or_object, obj_type)
        except ValueError:
            return None

    def _client_disconnected(self, event: Event, sender: str) -> bool:
        """Called when a client disconnects.

        Args:
            event: Disconnect event.
            sender: Name of client that disconnected.

        """

        # if a client disconnects, we remove its proxy
        if sender in self._proxies:
            del self._proxies[sender]
        return True

    @property
    def name(self) -> Optional[str]:
        """Name of this client."""
        raise NotImplementedError

    @property
    def clients(self) -> List[str]:
        """Returns list of currently connected clients.

        Returns:
            (list) List of currently connected clients.
        """
        raise NotImplementedError

    async def clients_with_interface(self, interface: Type[Interface]) -> List[str]:
        """Returns list of currently connected clients that implement the given interface.

        Args:
            interface: Interface to search for.

        Returns:
            (list) List of currently connected clients that implement the given interface.
        """
        return [c for c in self.clients if await self._supports_interface(c, interface)]

    async def get_interfaces(self, client: str) -> List[Type[Interface]]:
        """Returns list of interfaces for given client.

        Args:
            client: Name of client.

        Returns:
            List of supported interfaces.

        Raises:
            IndexError: If client cannot be found.
        """
        raise NotImplementedError

    async def _supports_interface(self, client: str, interface: Type[Interface]) -> bool:
        """Checks, whether the given client supports the given interface.

        Args:
            client: Client to check.
            interface: Interface to check.

        Returns:
            Whether or not interface is supported.
        """
        raise NotImplementedError

    @staticmethod
    def _interface_names_to_classes(interfaces: List[str]) -> List[Type[Interface]]:
        """Converts a list of interface names to interface classes.

        Args:
            interfaces: List of interface names.

        Returns:
            List of interface classes.
        """

        # get interface classes
        inspection = inspect.getmembers(pyobs.interfaces, predicate=inspect.isclass)

        # loop interfaces
        interface_classes = []
        for interface_name in interfaces:
            # loop all classes
            found = False
            for cls_name, cls in inspection:
                # class needs to face same name and implement Interface
                if interface_name == cls_name and issubclass(cls, Interface):
                    # found it!
                    found = True

                    # then add it to the list of all interfaces
                    interface_classes.append(cls)

                    # there can only be one...
                    break

            # not found?
            if not found:
                log.error('Could not find interface "%s" for client.', interface_name)
        return interface_classes

    def execute(self, client: str, method: str, signature: inspect.Signature, *args: Any) -> Future:
        """Execute a given method on a remote client.

        Args:
            client (str): ID of client.
            method (str): Method to call.
            signature: Method signature.
            *args: List of parameters for given method.

        Returns:
            Passes through return from method call.
        """
        raise NotImplementedError

    async def _logging(self) -> None:
        """Background thread for handling the logging."""
        # run until closing
        while not self._closing.is_set():
            # get item (maybe wait for it) and send it
            entry = await self._log_queue.get()
            await self.send_event(entry)

    def log_message(self, entry: LogEvent) -> None:
        """Send a log message to other clients.

        Args:
            entry (LogEvent): Log event to send.
        """
        self._log_queue.put_nowait(entry)

    async def send_event(self, event: Event) -> None:
        """Send an event to other clients.

        Args:
            event (Event): Event to send
        """
        pass

    async def register_event(self, event_class: Type[Event], handler: Optional[Callable[[Event, str], bool]] = None) \
            -> None:
        """Register an event type. If a handler is given, we also receive those events, otherwise we just
        send them.

        Args:
            event_class: Class of event to register.
            handler: Event handler method.
        """
        pass


__all__ = ['Comm']
