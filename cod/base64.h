/*
 * Base64 encoding/decoding (RFC1341)
 * Copyright (c) 2005, Jouni Malinen <j@w1.fi>
 *
 * This software may be distributed under the terms of the BSD license.
 * See README for more details.
 */

// preso da http://web.mit.edu/freebsd/head/contrib/wpa/src/utils/base64.h

#ifndef BASE64_H
#define BASE64_H

/**
 * base64_encode - Base64 encode
 * @src: Data to be encoded
 * @len: Length of the data to be encoded
 * @out_len: Pointer to output length variable, or %NULL if not used
 * Returns: Allocated buffer of out_len bytes of encoded data,
 * or %NULL on failure
 *
 * Caller is responsible for freeing the returned buffer
 */

unsigned char * base64_encode(const unsigned char *src, size_t len,
			      size_t *out_len);

// variante senza malloc
// dim(dst) = 4 * ceil(len/3)
size_t b64_encode(const void * src, size_t len, void * dst) ;


/**
 * base64_decode - Base64 decode
 * @src: Data to be decoded
 * @len: Length of the data to be decoded
 * @out_len: Pointer to output length variable
 * Returns: Allocated buffer of out_len bytes of decoded data,
 * or %NULL on failure
 *
 * Caller is responsible for freeing the returned buffer.
 */

unsigned char * base64_decode(const unsigned char *src, size_t len,
			      size_t *out_len);

// variante senza malloc
size_t b64_decode(const void * src, size_t len, void * dst) ;

#endif /* BASE64_H */
