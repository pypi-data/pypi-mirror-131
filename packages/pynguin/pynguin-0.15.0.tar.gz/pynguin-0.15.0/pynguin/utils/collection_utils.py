#  This file is part of Pynguin.
#
#  SPDX-FileCopyrightText: 2019–2021 Pynguin Contributors
#
#  SPDX-License-Identifier: LGPL-3.0-or-later
#
"""Utility methods for collections."""
from typing import Any, Dict, Set


def dict_without_keys(dict_to_change: Dict[Any, Any], keys: Set[Any]) -> Dict[Any, Any]:
    """
    Removes the given keys from the given dict.

    Args:
        dict_to_change: The dict where the keys should be removed.
        keys: The list of keys which should be removed.

    Returns:
        the dict without the specified keys.
    """
    return {k: v for k, v in dict_to_change.items() if k not in keys}
