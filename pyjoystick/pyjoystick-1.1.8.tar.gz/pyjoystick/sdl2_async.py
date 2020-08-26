import asyncio
import ctypes
from pyjoystick.sdl2 import sdl2, Joystick, get_init, init, key_from_event, stop_event_wait


async def get_async_event(event: sdl2.SDL_Event = None, alive=None) -> sdl2.SDL_Event:
    if alive is None:
        alive = lambda: True
    if event is None:
        event = sdl2.SDL_Event()

    # while True:
    #     if sdl2.SDL_PollEvent(ctypes.byref(event)):
    #         return
    #     else:
    #         await asyncio.sleep(0)

    loop = asyncio.get_running_loop()
    while alive():
        if await loop.run_in_executor(None, sdl2.SDL_WaitEventTimeout, ctypes.byref(event), 2000) != 0:
            return event
    return None


async def async_event_loop(add_joystick, remove_joystick, handle_key_event, alive=None, **kwargs):
    """Run the an event loop to process SDL Events.

    Args:
        add_joystick (callable/function): Called when a new Joystick is found!
        remove_joystick (callable/function): Called when a Joystick is removed!
        handle_key_event (callable/function): Called when a new key event occurs!
        alive (callable/function)[None]: Function to return True to continue running. If None run forever
    """
    if alive is None:
        alive = lambda: True

    if not get_init():
        init()

    event = sdl2.SDL_Event()
    while alive():
        result = await get_async_event(event, alive=alive)
        if result is None:
            break

        # Check the event
        if event.type == sdl2.SDL_JOYDEVICEADDED:
            try:
                # NOTE: event.jdevice.which is the id to use for SDL_JoystickOpen()
                joy = Joystick(identifier=event.jdevice.which)
                await add_joystick(joy)
            except:
                pass
        elif event.type == sdl2.SDL_JOYDEVICEREMOVED:
            try:
                # NOTE: event.jdevice.which is the id to use for SDL_JoystickFromInstanceID()
                joy = Joystick(instance_id=event.jdevice.which)
                await remove_joystick(joy)
            except:
                pass
        else:
            # NOTE: event.jdevice.which is the id to use for SDL_JoystickFromInstanceID()
            joy = Joystick(instance_id=event.jdevice.which)
            key = key_from_event(event, joy)
            if key is not None:
                await handle_key_event(key)


# Attach a way to stop waiting by posting an event
async_event_loop.stop_event_wait = stop_event_wait
