framedata_h_types_cdef = """

/* frame_data.h
 * Definitions for frame_data structures and routines
 *
 * Wireshark - Network traffic analyzer
 * By Gerald Combs <gerald@wireshark.org>
 * Copyright 1998 Gerald Combs
 *
 * SPDX-License-Identifier: GPL-2.0-or-later
 */


struct _packet_info;
struct epan_session;

/* Types of character encodings */
typedef enum {
  PACKET_CHAR_ENC_CHAR_ASCII     = 0, /* ASCII */
  PACKET_CHAR_ENC_CHAR_EBCDIC    = 1  /* EBCDIC */
} packet_char_enc;


/** The frame number is the ordinal number of the frame in the capture, so
   it's 1-origin.  In various contexts, 0 as a frame number means "frame
   number unknown".

   There is one of these structures for every frame in the capture.
   That means a lot of memory if we have a lot of frames.
   They are packed into power-of-2 chunks, so their size is effectively
   rounded up to a power of 2.
   Try to keep it close to, and less than or equal to, a power of 2.
   "Smaller than a power of 2" is OK for ILP32 platforms.

   XXX - shuffle the fields to try to keep the most commonly-accessed
   fields within the first 16 or 32 bytes, so they all fit in a cache
   line? */
struct _color_filter; /* Forward */

typedef struct _frame_data {
  guint32      num;          /**< Frame number */
  guint32      pkt_len;      /**< Packet length */
  guint32      cap_len;      /**< Amount actually captured */
  guint32      cum_bytes;    /**< Cumulative bytes into the capture */
  gint64       file_off;     /**< File offset */
  /* These two are pointers, meaning 64-bit on LP64 (64-bit UN*X) and
     LLP64 (64-bit Windows) platforms.  Put them here, one after the
     other, so they don't require padding between them. */
  GSList      *pfd;          /**< Per frame proto data */
  const struct _color_filter *color_filter;  /**< Per-packet matching color_filter_t object */
  guint16      subnum;       /**< subframe number, for protocols that require this */
  /* Keep the bitfields below to 16 bits, so this plus the previous field
     are 32 bits. */
  unsigned int passed_dfilter   : 1; /**< 1 = display, 0 = no display */
  unsigned int dependent_of_displayed : 1; /**< 1 if a displayed frame depends on this frame */
  /* Do NOT use packet_char_enc enum here: MSVC compiler does not handle an enum in a bit field properly */
  unsigned int encoding         : 1; /**< Character encoding (ASCII, EBCDIC...) */
  unsigned int visited          : 1; /**< Has this packet been visited yet? 1=Yes,0=No*/
  unsigned int marked           : 1; /**< 1 = marked by user, 0 = normal */
  unsigned int ref_time         : 1; /**< 1 = marked as a reference time frame, 0 = normal */
  unsigned int ignored          : 1; /**< 1 = ignore this frame, 0 = normal */
  unsigned int has_ts           : 1; /**< 1 = has time stamp, 0 = no time stamp */
  unsigned int has_phdr_comment : 1; /** 1 = there's comment for this packet */
  unsigned int has_user_comment : 1; /** 1 = user set (also deleted) comment for this packet */
  unsigned int need_colorize    : 1; /**< 1 = need to (re-)calculate packet color */
  unsigned int tsprec           : 4; /**< Time stamp precision -2^tsprec gives up to femtoseconds */
  nstime_t     abs_ts;       /**< Absolute timestamp */
  nstime_t     shift_offset; /**< How much the abs_tm of the frame is shifted */
  guint32      frame_ref_num; /**< Previous reference frame (0 if this is one) */
  guint32      prev_dis_num; /**< Previous displayed frame (0 if first one) */
} frame_data;
"""

framedata_h_funcs_cdef = """
/** compare two frame_datas */
extern gint frame_data_compare(const struct epan_session *epan, const frame_data *fdata1, const frame_data *fdata2, int field);

extern void frame_data_reset(frame_data *fdata);

extern void frame_data_destroy(frame_data *fdata);

extern void frame_data_init(frame_data *fdata, guint32 num,
                const wtap_rec *rec, gint64 offset,
                guint32 cum_bytes);

/* FIXME: Not exported by lib
extern void frame_delta_abs_time(const struct epan_session *epan, const frame_data *fdata,
                guint32 prev_num, nstime_t *delta);
*/
/**
 * Sets the frame data struct values before dissection.
 */
extern void frame_data_set_before_dissect(frame_data *fdata,
                nstime_t *elapsed_time,
                const frame_data **frame_ref,
                const frame_data *prev_dis);

extern void frame_data_set_after_dissect(frame_data *fdata,
                guint32 *cum_bytes);
"""
