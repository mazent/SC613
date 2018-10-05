/*
	per avere solo precise fault:

	#define DISDEFWBUF		(1 << 1)
	#define SCB_ACTLR		0xE000E008

	*(uint8_t *) SCB_ACTLR |= DISDEFWBUF ;
*/
#define STAMPA_DBG
#include "includimi.h"

void HardFault_Handler(void)
{
#ifdef NDEBUG
	NVIC_SystemReset() ;
#else
	uint32_t linkreg ;
	uint32_t * hardfaultStack = NULL ;

	__asm volatile( "mov %0, r14" : "=r"(linkreg) );
	switch (linkreg) {
	case 0xFFFFFFF1:
	case 0xFFFFFFF9:
		DBG_PUTS("stack MSP") ;
		hardfaultStack = (uint32_t *) __get_MSP() ;
		break ;
	case 0xFFFFFFFD:
		DBG_PUTS("stack PSP") ;
		hardfaultStack = (uint32_t *) __get_PSP() ;
		break ;
	default:
		DBG_PRINTF("EXC_RETURN ? 0x%08" PRIx32 "?\n", linkreg) ;
		break ;
	}

	if (hardfaultStack) {
		DBG_PRINTF("    %p\n", hardfaultStack) ;
	    DBG_PRINTF("    R0   = 0x%08" PRIx32 "\n", hardfaultStack[0]) ;
	    DBG_PRINTF("    R1   = 0x%08" PRIx32 "\n", hardfaultStack[1]) ;
	    DBG_PRINTF("    R2   = 0x%08" PRIx32 "\n", hardfaultStack[2]) ;
	    DBG_PRINTF("    R3   = 0x%08" PRIx32 "\n", hardfaultStack[3]) ;
	    DBG_PRINTF("    R12  = 0x%08" PRIx32 "\n", hardfaultStack[4]) ;
	    DBG_PRINTF("    LR   = 0x%08" PRIx32 "\n", hardfaultStack[5]) ;
	    DBG_PRINTF("    PC   = 0x%08" PRIx32 "\n", hardfaultStack[6]) ;
	    DBG_PRINTF("    xPSR = 0x%08" PRIx32 "\n", hardfaultStack[7]) ;
	}

//	uint32_t tmp ;
//	/*
//		0 = Thread mode
//		1 = Reserved
//		2 = NMI
//		3 = HardFault
//		4 = MemManage
//		5 = BusFault
//		6 = UsageFault
//		7-10 = Reserved
//		11 = SVCall
//		12 = Reserved for Debug
//		13 = Reserved
//		14 = PendSV
//		15 = SysTick
//		16 = IRQ0
//	*/
//	DBG_PRINTF("IPSR %d\n", (int) __get_IPSR()) ;
//
//	tmp = SCB->CFSR ;
//	DBG_PRINTF("CFSR %08X\n", tmp) ;
//	if (tmp & 0x000000FF) {
//		DBG_PUTS("    Memory Management Fault Status Register") ;
//		if (tmp & MMARVALID) {
//			// MMFAR holds a valid fault address
//			DBG_PRINTF("    MMFAR %08X\n", SCB->MMFAR) ;
//		}
//
//		if (tmp & MSTKERR) {
//			DBG_PUTS("        stacking for an exception entry has caused one or more access violations") ;
//		}
//
//		if (tmp & MUNSTKERR) {
//			DBG_PUTS("        unstack for an exception return has caused one or more access violations") ;
//		}
//
//		if (tmp & DACCVIOL) {
//			DBG_PUTS("        the processor attempted a load or store at a location that does not permit the operation") ;
//		}
//
//		if (tmp & IACCVIOL) {
//			DBG_PUTS("        the processor attempted an instruction fetch from a location that does not permit execution") ;
//		}
//	}
//	if (tmp & 0x0000FF00) {
//		uint32_t x = tmp >> 8 ;
//		DBG_PUTS("    Bus Fault Status Register") ;
//		if (x & BFARVALID) {
//			// BFAR holds a valid fault address.
//			DBG_PRINTF("        BFAR %08X\n", SCB->BFAR) ;
//		}
//		if (x & STKERR) {
//			DBG_PUTS("        stacking for an exception entry has caused one or more BusFaults") ;
//		}
//		if (x & UNSTKERR) {
//			DBG_PUTS("        unstack for an exception return has caused one or more BusFaults") ;
//		}
//		if (x & IMPRECISERR) {
//			DBG_PUTS("        a data bus error has occurred, but the return address in the stack frame is not related to the instruction that caused the error") ;
//		}
//		if (x & PRECISERR) {
//			DBG_PUTS("        a data bus error has occurred, and the PC value stacked for the exception return points to the instruction that caused the fault") ;
//		}
//		if (x & IBUSERR) {
//			DBG_PUTS("        instruction bus error") ;
//		}
//	}
//	if (tmp & 0xFFFF0000) {
//		uint32_t x = tmp >> 16 ;
//
//		DBG_PUTS("    Usage Fault Status Register") ;
//
//		if (x & DIVBYZERO) {
//			DBG_PUTS("        the processor has executed an SDIV or UDIV instruction with a divisor of 0") ;
//		}
//		if (x & UNALIGNED) {
//			DBG_PUTS("        the processor has made an unaligned memory access") ;
//		}
//		if (x & NOCP) {
//			DBG_PUTS("        the processor has attempted to access a coprocessor") ;
//		}
//		if (x & INVPC) {
//			DBG_PUTS("        the processor has attempted an illegal load of EXC_RETURN to the PC, as a result of an invalid context, or an invalid EXC_RETURN value") ;
//		}
//		if (x & INVSTATE) {
//			DBG_PUTS("        the processor has attempted to execute an instruction that makes illegal use of the EPSR") ;
//		}
//		if (x & UNDEFINSTR) {
//			DBG_PUTS("        the processor has attempted to execute an undefined instruction") ;
//		}
//	}
//
//	tmp = SCB->HFSR ;
//	DBG_PRINTF("HFSR %08X\n", tmp) ;
//	if (tmp & FORCED) {
//		DBG_PUTS("    forced HardFault") ;
//	}
//	if (tmp & VECTTBL) {
//		DBG_PUTS("    BusFault on vector table read") ;
//	}
//
//	DBG_PRINTF("AFSR %08X\n", SCB->AFSR) ;

	__BKPT(0) ;
#endif
}

