wsutil_privileges_h_funcs_cdef = """

/* privileges.h
 * Declarations of routines for handling privileges.
 *
 * Wireshark - Network traffic analyzer
 * By Gerald Combs <gerald@wireshark.org>
 * Copyright 2006 Gerald Combs
 *
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

/**
 * Called when the program starts, to enable security features and save
 * whatever credential information we'll need later.
 */
extern void init_process_policies(void);

/**
 * Was this program started with special privileges?  get_credential_info()
 * MUST be called before calling this.
 * @return TRUE if the program was started with special privileges,
 * FALSE otherwise.
 */
extern gboolean started_with_special_privs(void);

/**
 * Is this program running with special privileges? get_credential_info()
 * MUST be called before calling this.
 * @return TRUE if the program is running with special privileges,
 * FALSE otherwise.
 */
extern gboolean running_with_special_privs(void);

/**
 * Permanently relinquish special privileges. get_credential_info()
 * MUST be called before calling this.
 */
extern void relinquish_special_privs_perm(void);

/**
 * Get the current username.  String must be g_free()d after use.
 * @return A freshly g_alloc()ed string containing the username,
 * or "UNKNOWN" on failure.
 */
extern gchar *get_cur_username(void);

/**
 * Get the current group.  String must be g_free()d after use.
 * @return A freshly g_alloc()ed string containing the group,
 * or "UNKNOWN" on failure.
 */
extern gchar *get_cur_groupname(void);

"""
