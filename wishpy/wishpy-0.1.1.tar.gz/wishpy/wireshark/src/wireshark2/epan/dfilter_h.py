epan_dfilter_h_types_cdef = """
/*
 * Wireshark - Network traffic analyzer
 * By Gerald Combs <gerald@wireshark.org>
 * Copyright 2001 Gerald Combs
 *
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

/* Passed back to user */
typedef struct epan_dfilter dfilter_t;

struct epan_dissect;
"""

epan_dfilter_h_funcs_cdef = """

/* Compiles a string to a dfilter_t.
 * On success, sets the dfilter* pointed to by dfp
 * to either a NULL pointer (if the filter is a null
 * filter, as generated by an all-blank string) or to
 * a pointer to the newly-allocated dfilter_t
 * structure.
 *
 * On failure, *err_msg is set to point to the error
 * message.  This error message is allocated with
 * g_malloc(), and must be freed with g_free().
 * The dfilter* will be set to NULL after a failure.
 *
 * Returns TRUE on success, FALSE on failure.
 */

extern
gboolean
dfilter_compile(const gchar *text, dfilter_t **dfp, gchar **err_msg);

/* Frees all memory used by dfilter, and frees
 * the dfilter itself. */
extern
void
dfilter_free(dfilter_t *df);

/* Apply compiled dfilter */
extern
gboolean
dfilter_apply_edt(dfilter_t *df, struct epan_dissect *edt);

extern
GPtrArray *
dfilter_deprecated_tokens(dfilter_t *df);

/* Print bytecode of dfilter to stdout */
extern
void
dfilter_dump(dfilter_t *df);

"""
