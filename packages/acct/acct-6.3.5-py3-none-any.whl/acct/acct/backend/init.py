from typing import Any
from typing import Dict
from typing import Iterable

import dict_tools.update
from dict_tools.data import NamespaceDict


async def unlock(hub, profiles: Dict[str, Dict[str, Any]], backend_key: str = None):
    """
    Read the raw profiles and search for externally defined profiles.
    """
    # Allow custom specification of a backend key per acct_file
    if backend_key is None:
        backend_key = profiles.get("backend_key", hub.acct.BACKEND_KEY)

    ret = {}
    for backend, backend_profile_data in profiles.get(backend_key, {}).items():
        if backend not in hub.acct.backend:
            hub.log.error(f"acct backend '{backend}' is not available")
            continue
        # The keys are irrelevant for backend profiles
        for ctx in backend_profile_data.values():
            try:
                hub.log.info(f"Reading acct backend profiles from '{backend}'")
                backend_profiles = hub.acct.backend[backend].unlock(**ctx)
                backend_profiles = await hub.pop.loop.unwrap(backend_profiles)

                dict_tools.update.update(ret, backend_profiles)
            except Exception as e:
                hub.log.error(f"{e.__class__}: {e}")

    return ret


async def process(hub, subs: Iterable[str], profiles: Dict[str, Any]):
    """
    Process the given profiles through acct plugins.
    Acct plugins turn static profile data into connections to a server etc...
    """
    processed = NamespaceDict()
    for sub in subs:
        if not hasattr(hub.acct, sub):
            hub.log.trace(f"{sub} does not extend acct")
            continue

        processed[sub] = {}
        for plug in hub.acct[sub]:
            if "profiles" in plug.gather.signature.parameters:
                ret = plug.gather(profiles)
            else:
                # It either doesn't need to know about existing profiles or will get them from hub.acct.PROFILES
                ret = plug.gather()

            ret = await hub.pop.loop.unwrap(ret)

            processed[sub][plug.__name__] = ret
    return processed
