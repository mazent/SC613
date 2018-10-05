/*
 * Base64 encoding/decoding (RFC1341)
 * Copyright (c) 2005-2011, Jouni Malinen <j@w1.fi>
 *
 * This software may be distributed under the terms of the BSD license.
 * See README for more details.
 */

// preso da http://web.mit.edu/freebsd/head/contrib/wpa/src/utils/base64.c

#include "includimi.h"
#include "base64.h"

#define os_malloc	malloc
#define os_free		free

static const unsigned char base64_table[65] =
	"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

unsigned char * base64_encode(const unsigned char *src, size_t len,
			      size_t *out_len)
{
	unsigned char *out, *pos;
	const unsigned char *end, *in;
	size_t olen;

	olen = len * 4 / 3 + 4; /* 3-byte blocks to 4-byte */
	if (olen < len)
		return NULL; /* integer overflow */
	out = os_malloc(olen);
	if (out == NULL)
		return NULL;

	end = src + len;
	in = src;
	pos = out;
	while (end - in >= 3) {
		*pos++ = base64_table[in[0] >> 2];
		*pos++ = base64_table[((in[0] & 0x03) << 4) | (in[1] >> 4)];
		*pos++ = base64_table[((in[1] & 0x0f) << 2) | (in[2] >> 6)];
		*pos++ = base64_table[in[2] & 0x3f];
		in += 3;
	}

	if (end - in) {
		*pos++ = base64_table[in[0] >> 2];
		if (end - in == 1) {
			*pos++ = base64_table[(in[0] & 0x03) << 4];
			*pos++ = '=';
		} else {
			*pos++ = base64_table[((in[0] & 0x03) << 4) |
					      (in[1] >> 4)];
			*pos++ = base64_table[(in[1] & 0x0f) << 2];
		}
		*pos++ = '=';
	}

	if (out_len)
		*out_len = pos - out;
	return out;
}

size_t b64_encode(const void * s, size_t len, void * o)
{
	uint8_t *pos;
	const uint8_t *end, *in;
	size_t olen;

	const uint8_t * src = (const uint8_t *) s ;
	uint8_t * out = (uint8_t *) o ;

	if (NULL == src)
		return 0 ;
	if (0 == len)
		return 0 ;
	if (out == NULL)
		return 0 ;

	olen = len * 4 / 3 + 4; /* 3-byte blocks to 4-byte */
	if (olen < len)
		return 0 ;

	end = src + len;
	in = src;
	pos = out;
	while (end - in >= 3) {
		*pos++ = base64_table[in[0] >> 2];
		*pos++ = base64_table[((in[0] & 0x03) << 4) | (in[1] >> 4)];
		*pos++ = base64_table[((in[1] & 0x0f) << 2) | (in[2] >> 6)];
		*pos++ = base64_table[in[2] & 0x3f];
		in += 3;
	}

	if (end - in) {
		*pos++ = base64_table[in[0] >> 2];
		if (end - in == 1) {
			*pos++ = base64_table[(in[0] & 0x03) << 4];
			*pos++ = '=';
		} else {
			*pos++ = base64_table[((in[0] & 0x03) << 4) |
					      (in[1] >> 4)];
			*pos++ = base64_table[(in[1] & 0x0f) << 2];
		}
		*pos++ = '=';
	}

	return pos - out ;
}

static const int B64index[256] =
{
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  62, 63, 62, 62, 63,
    52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 0,  0,  0,  0,  0,  0,
    0,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12, 13, 14,
    15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 0,  0,  0,  0,  63,
    0,  26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
    41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51
};

// presa da https://stackoverflow.com/questions/180947/base64-decode-snippet-in-c/13935718
unsigned char * base64_decode(const unsigned char *data, size_t len,
			      size_t *out_len)
{
    if (len == 0) return NULL;

    unsigned char *p = (unsigned char*) data;
    size_t j = 0,
        pad1 = len % 4 || p[len - 1] == '=',
        pad2 = pad1 && (len % 4 > 2 || p[len - 2] != '=');
    const size_t last = (len - pad1) / 4 << 2;

    *out_len = last / 4 * 3 + pad1 + pad2 ;

    unsigned char *str = os_malloc(last / 4 * 3 + pad1 + pad2) ;

    for (size_t i = 0; i < last; i += 4)
    {
        int n = B64index[p[i]] << 18 | B64index[p[i + 1]] << 12 | B64index[p[i + 2]] << 6 | B64index[p[i + 3]];
        str[j++] = n >> 16;
        str[j++] = n >> 8 & 0xFF;
        str[j++] = n & 0xFF;
    }
    if (pad1)
    {
        int n = B64index[p[last]] << 18 | B64index[p[last + 1]] << 12;
        str[j++] = n >> 16;
        if (pad2)
        {
            n |= B64index[p[last + 2]] << 6;
            str[j++] = n >> 8 & 0xFF;
        }
    }

    return str ;
}

size_t b64_decode(const void * data, size_t len, void * dst)
{
	if (NULL == data)
		return 0 ;
	if (0 == len)
		return 0 ;
	if (dst == NULL)
		return 0 ;

    const unsigned char *p = (const unsigned char*) data;
    size_t j = 0,
        pad1 = len % 4 || p[len - 1] == '=',
        pad2 = pad1 && (len % 4 > 2 || p[len - 2] != '=');
    const size_t last = (len - pad1) / 4 << 2;

    size_t out_len = last / 4 * 3 + pad1 + pad2 ;

    unsigned char *str = (unsigned char *) dst ;

    for (size_t i = 0; i < last; i += 4)
    {
        int n = B64index[p[i]] << 18 | B64index[p[i + 1]] << 12 | B64index[p[i + 2]] << 6 | B64index[p[i + 3]];
        str[j++] = n >> 16;
        str[j++] = n >> 8 & 0xFF;
        str[j++] = n & 0xFF;
    }
    if (pad1)
    {
        int n = B64index[p[last]] << 18 | B64index[p[last + 1]] << 12;
        str[j++] = n >> 16;
        if (pad2)
        {
            n |= B64index[p[last + 2]] << 6;
            str[j++] = n >> 8 & 0xFF;
        }
    }

    return out_len ;
}


//unsigned char * base64_decode(const unsigned char *src, size_t len,
//			      size_t *out_len)
//{
//	static unsigned char dtable[256] ;
//	static bool init = false ;
//	unsigned char *out, *pos, block[4], tmp;
//	size_t i, count, olen;
//	int pad = 0;
//
//	if (!init) {
//		os_memset(dtable, 0x80, 256);
//		for (i = 0; i < sizeof(base64_table) - 1; i++)
//			dtable[base64_table[i]] = (unsigned char) i;
//		dtable['='] = 0;
//
//		init = true ;
//	}
//
//	count = 0;
//	for (i = 0; i < len; i++) {
//		if (dtable[src[i]] != 0x80)
//			count++;
//	}
//
//	if (count == 0 || count % 4)
//		return NULL;
//
//	olen = count / 4 * 3;
//	pos = out = os_malloc(olen);
//	if (out == NULL)
//		return NULL;
//
//	count = 0;
//	for (i = 0; i < len; i++) {
//		tmp = dtable[src[i]];
//		if (tmp == 0x80)
//			continue;
//
//		if (src[i] == '=')
//			pad++;
//		block[count] = tmp;
//		count++;
//		if (count == 4) {
//			*pos++ = (block[0] << 2) | (block[1] >> 4);
//			*pos++ = (block[1] << 4) | (block[2] >> 2);
//			*pos++ = (block[2] << 6) | block[3];
//			count = 0;
//			if (pad) {
//				if (pad == 1)
//					pos--;
//				else if (pad == 2)
//					pos -= 2;
//				else {
//					/* Invalid padding */
//					os_free(out);
//					return NULL;
//				}
//				break;
//			}
//		}
//	}
//
//	*out_len = pos - out;
//	return out;
//}

#if 0

void base64_test(void)
{
    uint8_t x[] = { 0x2C, 0x90, 0xC7, 0xE0, 0x5F, 0xF5, 0x8E, 0x83, 0xB9, 0xFD } ;
    int ciclo = 1 ;

    while (true) {
    	DBG_PRINTF("ciclo %d\n", ciclo) ;
    	++ciclo ;

    	for (int i=1 ; i<sizeof(x) ; i++) {
    		size_t dimc, dimd ;
        	unsigned char * cod = base64_encode(x, i, &dimc) ;
        	unsigned char * dec = base64_decode(cod, dimc, &dimd) ;

        	if (dimd != i) {
        		DBG_ERR ;
        	}
        	else if (0 != memcmp(dec, x, i)) {
        		DBG_ERR ;
        	}

        	free(cod) ;
        	free(dec) ;
    	}

    	for (int i=0 ; i<sizeof(x) ; i++)
    		++x[i] ;
    }
}

#elif 0

void base64_test(void)
{
    uint8_t x[] = { 0x2C, 0x90, 0xC7, 0xE0, 0x5F, 0xF5, 0x8E, 0x83, 0xB9, 0xFD } ;
    uint8_t cod[16], dec[16] ;
    int ciclo = 1 ;

    while (true) {
    	DBG_PRINTF("ciclo %d\n", ciclo) ;
    	++ciclo ;

    	for (int i=1 ; i<sizeof(x) ; i++) {
    		size_t dimc = b64_encode(x, i, cod) ;
    		size_t dimd = b64_decode(cod, dimc, dec) ;

        	if (dimd != i) {
        		DBG_ERR ;
        	}
        	else if (0 != memcmp(dec, x, i)) {
        		DBG_ERR ;
        	}
    	}

    	for (int i=0 ; i<sizeof(x) ; i++)
    		++x[i] ;
    }
}

#endif

