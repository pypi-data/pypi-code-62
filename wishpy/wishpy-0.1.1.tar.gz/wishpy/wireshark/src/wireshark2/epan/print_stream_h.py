epan_print_stream_h_types_cdef = """
/* print_stream.h
 * Definitions for print streams.
 *
 * Gilbert Ramirez <gram@alumni.rice.edu>
 *
 * Wireshark - Network traffic analyzer
 * By Gerald Combs <gerald@wireshark.org>
 * Copyright 1998 Gerald Combs
 *
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

/*
 * Print stream code; this provides a "print stream" class with subclasses
 * of various sorts.  Additional subclasses might be implemented elsewhere.
 */
struct print_stream;

typedef struct print_stream_ops {
	gboolean (*print_preamble)(struct print_stream *self, gchar *filename, const char *version_string);
	gboolean (*print_line)(struct print_stream *self, int indent,
	    const char *line);
	gboolean (*print_bookmark)(struct print_stream *self,
	    const gchar *name, const gchar *title);
	gboolean (*new_page)(struct print_stream *self);
	gboolean (*print_finale)(struct print_stream *self);
	gboolean (*destroy)(struct print_stream *self);
	gboolean (*print_line_color)(struct print_stream *self, int indent, const char *line, const color_t *fg, const color_t *bg);
} print_stream_ops_t;

typedef struct print_stream {
	const print_stream_ops_t *ops;
	void *data;
} print_stream_t;

"""

epan_print_stream_h_funcs_cdef = """
extern print_stream_t *print_stream_text_new(gboolean to_file, const char *dest);
extern print_stream_t *print_stream_text_stdio_new(FILE *fh);
extern print_stream_t *print_stream_ps_new(gboolean to_file, const char *dest);
extern print_stream_t *print_stream_ps_stdio_new(FILE *fh);

extern gboolean print_preamble(print_stream_t *self, gchar *filename, const char *version_string);
extern gboolean print_line(print_stream_t *self, int indent, const char *line);
extern gboolean print_bookmark(print_stream_t *self, const gchar *name,
    const gchar *title);
extern gboolean new_page(print_stream_t *self);
extern gboolean print_finale(print_stream_t *self);
extern gboolean destroy_print_stream(print_stream_t *self);

/*
 * equivalent to print_line(), but if the stream supports text coloring then
 * the output text will also be colored with the given foreground and
 * background
 *
 * returns TRUE if the print was successful, FALSE otherwise
 */
extern gboolean print_line_color(print_stream_t *self, int indent, const char *line, const color_t *fg, const color_t *bg);

"""
