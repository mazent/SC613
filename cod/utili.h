#ifndef UTILI_H_
#define UTILI_H_

/********************************************
    Inclusione di varie cose utili
********************************************/

// Questi mancano
// ==========================================

#define MINI(a, b)			((a) < (b) ? (a) : (b))
#define MAXI(a, b)			((a) > (b) ? (a) : (b))

#define INUTILE(x)          (void)(sizeof(x))
#define NEGA(x)             (~(unsigned int) (x))

typedef uint32_t DWORD ;
typedef uint16_t WORD ;
typedef uint8_t  BYTE ;

// Varie
// ==========================================

    // Conversione a stringa (token stringification)
    //      #define foo 4
    //      STRINGA(foo)  -> "foo"
    //      STRINGA2(foo) -> "4"    
#define STRINGA(a)       #a
#define STRINGA2(a)      STRINGA(a)

    // La assert() viene eliminata in release, invece io
    // voglio mantenere il controllo generando un reset
    // se qualcosa va male
#ifdef NDEBUG      
#   define ASSERT(a)        if ( !(a) ) NVIC_SystemReset()
#   define CONTROLLA(a)     (void)(a)
#else 
#   define ASSERT(a)        assert(a)
#   define CONTROLLA(a)     assert(a)
#endif

#define DIM_VETT(a)         sizeof(a) / sizeof(a[0])

// TerminalIO
// ==========================================

#ifdef NDEBUG
	// In release non stampo mai
#	define PRINTF(f, ...)
#	define PUTS(a)

#   define BPOINT
#else
	// In debug e' utile stampare
#   include <stdio.h>

#	define PRINTF(f, ...)	printf(f, ##__VA_ARGS__)
#	define PUTS(a)			puts(a)

#   define BPOINT       	__BKPT(0)
#endif

	// Alcune stampe possono essere disabilitate
#ifdef STAMPA_DBG
#	define DBG_ERR						PRINTF("ERR %s %d\n", __FILE__, __LINE__)
#	define DBG_PRINTF(f, ...)			PRINTF(f, ##__VA_ARGS__)
#	define DBG_PUTS(a)					PUTS(a)
#else
#	define DBG_ERR
#	define DBG_PRINTF(f, ...)
#	define DBG_PUTS(a)
#endif

// Quindi se ...
#if defined(STAMPA_DBG) && !defined(NDEBUG)
	// ... le DBG_?? sono abilitate
#	define DBG_ABIL		1
#endif



#endif
