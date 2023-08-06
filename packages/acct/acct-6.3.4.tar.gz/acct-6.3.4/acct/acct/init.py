import sys
from typing import Any
from typing import Dict
from typing import Iterable

import dict_tools.update
from dict_tools.data import NamespaceDict

__func_alias__ = {"profiles_": "profiles"}


def __init__(hub):
    hub.acct.PROFILES = NamespaceDict()
    hub.acct.SUB_PROFILES = NamespaceDict()
    hub.acct.UNLOCKED = False
    hub.acct.DEFAULT = "default"
    hub.acct.BACKEND_KEY = "acct-backends"

    hub.pop.sub.add(dyne_name="crypto")
    hub.pop.sub.load_subdirs(hub.acct, recurse=True)


def cli(hub):
    hub.pop.sub.add(dyne_name="rend")
    hub.pop.config.load(["acct", "rend"], cli="acct")
    hub.pop.loop.create()
    coro = hub.acct.init.cli_apply()
    retcode = hub.pop.Loop.run_until_complete(coro)
    sys.exit(retcode)


async def cli_apply(hub) -> int:
    if hub.SUBPARSER == "encrypt":
        created_new_acct_key = False
        if not hub.OPT.acct.acct_key:
            created_new_acct_key = True
            hub.log.info(
                f"New acct_key generated with '{hub.OPT.acct.crypto_plugin}' plugin"
            )

        new_key = await hub.crypto.init.encrypt_file(
            crypto_plugin=hub.OPT.acct.crypto_plugin,
            acct_file=hub.OPT.acct.input_file,
            acct_key=hub.OPT.acct.acct_key,
            output_file=hub.OPT.acct.output_file,
        )
        hub.log.info(
            f"Encrypted {hub.OPT.acct.input_file} with the {hub.OPT.acct.crypto_plugin} algorithm"
        )
        if created_new_acct_key:
            # Print this to the terminal, and only this -- for easier scripting
            # Do not log it or put it in log files
            print(new_key)

        return 0
    elif hub.SUBPARSER == "decrypt":
        ret = await hub.crypto.init.decrypt_file(
            crypto_plugin=hub.OPT.acct.crypto_plugin,
            acct_file=hub.OPT.acct.input_file,
            acct_key=hub.OPT.acct.acct_key,
        )
        outputter = hub.OPT.rend.output or "yaml"
        out = hub.output[outputter].display(ret)
        print(out)
        return 0


async def profiles_(
    hub, acct_file: str, acct_key: str, crypto_plugin: str = "fernet"
) -> Dict[str, Any]:
    """
    Read profile information from a file and return the raw data
    """
    raw_profiles = await hub.crypto.init.decrypt_file(
        crypto_plugin=crypto_plugin,
        acct_file=acct_file,
        acct_key=acct_key,
    )
    backend_profiles = await hub.acct.backend.init.unlock(profiles=raw_profiles)
    dict_tools.update.update(raw_profiles, backend_profiles)
    return raw_profiles


async def unlock(hub, acct_file: str, acct_key: str, crypto_plugin: str = "fernet"):
    """
    Initialize the file read, then store the authentication data on the hub as hub.acct.PROFILES
    """
    if hub.acct.UNLOCKED:
        return

    raw_profiles = await hub.acct.init.profiles(acct_file, acct_key, crypto_plugin)
    hub.acct.BACKEND_KEY = raw_profiles.pop("backend_key", hub.acct.BACKEND_KEY)
    hub.acct.DEFAULT = raw_profiles.pop("default", hub.acct.DEFAULT)
    dict_tools.update.update(hub.acct.PROFILES, raw_profiles)
    hub.acct.UNLOCKED = True


async def unlock_blob(
    hub,
    acct_file_contents: str,
    acct_key: str,
    crypto_plugin: str = "fernet",
    backend_key: str = None,
    default_profile: str = None,
):
    raw_profiles = await hub.crypto.init.decrypt(
        crypto_plugin, acct_file_contents, acct_key
    )
    if backend_key is None:
        backend_key = raw_profiles.get("backend_key", hub.acct.BACKEND_KEY)
    backend_profiles = await hub.acct.backend.init.unlock(
        profiles=raw_profiles, backend_key=backend_key
    )

    if default_profile is None:
        default_profile = raw_profiles.get("default", hub.acct.DEFAULT)

    return NamespaceDict(
        default_profile=default_profile,
        backend_key=backend_key,
        sub_profiles=backend_profiles,
        profiles=raw_profiles,
    )


async def single(
    hub,
    profile_name: str,
    subs: Iterable[str],
    sub_profiles: Dict[str, Dict[str, Any]],
    profiles: Dict[str, Dict[str, Any]],
):
    """
    Retrieve a specific named profile for the given subs, sub_profiles, and profiles
    """
    ret = NamespaceDict()

    for sub, plugin in sub_profiles.items():
        for sub_data in plugin.values():
            if not sub_data:
                continue
            if profile_name in sub_data:
                dict_tools.update.update(ret, sub_data[profile_name])
    for sub in subs:
        if sub in profiles:
            if profile_name in profiles[sub]:
                dict_tools.update.update(ret, profiles[sub][profile_name])

    return ret


async def gather(
    hub, subs: Iterable[str], profile: str, profiles=None, sub_profiles=None
) -> Dict[str, Dict[str, Any]]:
    """
    :param hub:
    :param subs: The subs to check for a profile
    :param profile: The name of the acct_profile to retrieve
    :param profiles: raw profiles to use if not unlocking acct first
    :param sub_profiles: sub profiles to use if not unlocking acct first
    :return: The named profile
    """
    # If acct is locked and we don't have new profiles then return right away
    if not hub.acct.UNLOCKED and not (profiles or sub_profiles):
        return {}

    # Use the profiles stored on the hub
    if profiles is None:
        profiles = hub.acct.PROFILES

    # Use the sub_profiles stored on the hub
    if sub_profiles is None:
        sub_profiles = hub.acct.SUB_PROFILES

    backend_key = profiles.get("backend_key", hub.acct.BACKEND_KEY)
    if backend_key in profiles:
        # Find any new sub_profiles from acct backends
        new_profiles = await hub.acct.backend.init.process(subs, sub_profiles)

        backend_profiles = await hub.acct.backend.init.unlock(new_profiles)
        dict_tools.update.update(new_profiles, backend_profiles)

        # Add the new profiles to the sub_profiles
        dict_tools.update.update(sub_profiles, new_profiles)

        if hub.acct.UNLOCKED:
            if not (profiles or sub_profiles):
                # If no new profiles were passed then assume we are working with the stored profiles only and update
                dict_tools.update.update(hub.acct.SUB_PROFILES, new_profiles)

        # Update the profiles that will be returned
        dict_tools.update.update(profiles, hub.acct.PROFILES)
        dict_tools.update.update(sub_profiles, hub.acct.SUB_PROFILES)

    return await hub.acct.init.single(
        profile_name=profile,
        subs=subs,
        profiles=profiles,
        sub_profiles=sub_profiles,
    )


async def close(hub):
    for sub, plugins in hub.acct.SUB_PROFILES.items():
        for plugin, profiles in plugins.items():
            if not hasattr(hub.acct[sub][plugin], "close"):
                continue

            ret = hub.acct[sub][plugin].close(profiles)
            await hub.pop.loop.unwrap(ret)
