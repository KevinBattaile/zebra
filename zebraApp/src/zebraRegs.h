/* Register map for zebra */

#ifndef __ZEBRAREGS_H__
#define __ZEBRAREGS_H__

enum regType {
    regRW,
    regRO,
    regCmd,
    regMux
};

/* This is a lookup table of string->register number */
struct reg {
    const char * str;
    int addr;
    regType type;
};

static const struct reg reg_lookup[] = {
    /* Which encoders/divs + system bus to capture in pos comp */
    /* Put this first as it is vital for decoding interrupts */
    { "PC_BIT_CAP",      0x9F, regRW },
    /* AND4 gate */
    { "AND1_INV",        0x00, regRW },
    { "AND2_INV",        0x01, regRW },
    { "AND3_INV",        0x02, regRW },
    { "AND4_INV",        0x03, regRW },
    { "AND1_ENA",        0x04, regRW },
    { "AND2_ENA",        0x05, regRW },
    { "AND3_ENA",        0x06, regRW },
    { "AND4_ENA",        0x07, regRW },
    { "AND1_INP1",       0x08, regMux },
    { "AND1_INP2",       0x09, regMux },
    { "AND1_INP3",       0x0A, regMux },
    { "AND1_INP4",       0x0B, regMux },
    { "AND2_INP1",       0x0C, regMux },
    { "AND2_INP2",       0x0D, regMux },
    { "AND2_INP3",       0x0E, regMux },
    { "AND2_INP4",       0x0F, regMux },
    { "AND3_INP1",       0x10, regMux },
    { "AND3_INP2",       0x11, regMux },
    { "AND3_INP3",       0x12, regMux },
    { "AND3_INP4",       0x13, regMux },
    { "AND4_INP1",       0x14, regMux },
    { "AND4_INP2",       0x15, regMux },
    { "AND4_INP3",       0x16, regMux },
    { "AND4_INP4",       0x17, regMux },
    /* OR4 gate */
    { "OR1_INV",         0x18, regRW },
    { "OR2_INV",         0x19, regRW },
    { "OR3_INV",         0x1A, regRW },
    { "OR4_INV",         0x1B, regRW },
    { "OR1_ENA",         0x1C, regRW },
    { "OR2_ENA",         0x1D, regRW },
    { "OR3_ENA",         0x1E, regRW },
    { "OR4_ENA",         0x1F, regRW },
    { "OR1_INP1",        0x20, regMux },
    { "OR1_INP2",        0x21, regMux },
    { "OR1_INP3",        0x22, regMux },
    { "OR1_INP4",        0x23, regMux },
    { "OR2_INP1",        0x24, regMux },
    { "OR2_INP2",        0x25, regMux },
    { "OR2_INP3",        0x26, regMux },
    { "OR2_INP4",        0x27, regMux },
    { "OR3_INP1",        0x28, regMux },
    { "OR3_INP2",        0x29, regMux },
    { "OR3_INP3",        0x2A, regMux },
    { "OR3_INP4",        0x2B, regMux },
    { "OR4_INP1",        0x2C, regMux },
    { "OR4_INP2",        0x2D, regMux },
    { "OR4_INP3",        0x2E, regMux },
    { "OR4_INP4",        0x2F, regMux },
    /* Gate generator */
    { "GATE1_INP1",      0x30, regMux },
    { "GATE2_INP1",      0x31, regMux },
    { "GATE3_INP1",      0x32, regMux },
    { "GATE4_INP1",      0x33, regMux },
    { "GATE1_INP2",      0x34, regMux },
    { "GATE2_INP2",      0x35, regMux },
    { "GATE3_INP2",      0x36, regMux },
    { "GATE4_INP2",      0x37, regMux },
    /* Pulse divider */
    { "DIV1_DIVLO",      0x38, regRW },
    { "DIV1_DIVHI",      0x39, regRW },
    { "DIV2_DIVLO",      0x3A, regRW },
    { "DIV2_DIVHI",      0x3B, regRW },
    { "DIV3_DIVLO",      0x3C, regRW },
    { "DIV3_DIVHI",      0x3D, regRW },
    { "DIV4_DIVLO",      0x3E, regRW },
    { "DIV4_DIVHI",      0x3F, regRW },
    { "DIV1_INP",        0x40, regMux },
    { "DIV2_INP",        0x41, regMux },
    { "DIV3_INP",        0x42, regMux },
    { "DIV4_INP",        0x43, regMux },
    /* Pulse generator */
    { "PULSE1_DLY",      0x44, regRW },
    { "PULSE2_DLY",      0x45, regRW },
    { "PULSE3_DLY",      0x46, regRW },
    { "PULSE4_DLY",      0x47, regRW },
    { "PULSE1_WID",      0x48, regRW },
    { "PULSE2_WID",      0x49, regRW },
    { "PULSE3_WID",      0x4A, regRW },
    { "PULSE4_WID",      0x4B, regRW },
    { "PULSE1_PRE",      0x4C, regRW },
    { "PULSE2_PRE",      0x4D, regRW },
    { "PULSE3_PRE",      0x4E, regRW },
    { "PULSE4_PRE",      0x4F, regRW },
    { "PULSE1_INP",      0x50, regMux },
    { "PULSE2_INP",      0x51, regMux },
    { "PULSE3_INP",      0x52, regMux },
    { "PULSE4_INP",      0x53, regMux },
    { "POLARITY",        0x54, regRW },
    /* Quadrature encoder */
    { "QUAD_DIR",        0x55, regMux },
    { "QUAD_STEP",       0x56, regMux },
    /* External inputs for Arm, Gate, Pulse */
    { "PC_ARM_INP",      0x57, regMux },
    { "PC_GATE_INP",     0x58, regMux },
    { "PC_PULSE_INP",    0x59, regMux },
    /* Output multiplexer select */
    { "OUT1_TTL",        0x60, regMux },
    { "OUT1_NIM",        0x61, regMux },
    { "OUT1_LVDS",       0x62, regMux },
    { "OUT2_TTL",        0x63, regMux },
    { "OUT2_NIM",        0x64, regMux },
    { "OUT2_LVDS",       0x65, regMux },
    { "OUT3_TTL",        0x66, regMux },
    { "OUT3_OC",         0x67, regMux },
    { "OUT3_LVDS",       0x68, regMux },
    { "OUT4_TTL",        0x69, regMux },
    { "OUT4_NIM",        0x6A, regMux },
    { "OUT4_PECL",       0x6B, regMux },
    { "OUT5_ENCA",       0x6C, regMux },
    { "OUT5_ENCB",       0x6D, regMux },
    { "OUT5_ENCZ",       0x6E, regMux },
    { "OUT5_CONN",       0x6F, regMux },
    { "OUT6_ENCA",       0x70, regMux },
    { "OUT6_ENCB",       0x71, regMux },
    { "OUT6_ENCZ",       0x72, regMux },
    { "OUT6_CONN",       0x73, regMux },
    { "OUT7_ENCA",       0x74, regMux },
    { "OUT7_ENCB",       0x75, regMux },
    { "OUT7_ENCZ",       0x76, regMux },
    { "OUT7_CONN",       0x77, regMux },
    { "OUT8_ENCA",       0x78, regMux },
    { "OUT8_ENCB",       0x79, regMux },
    { "OUT8_ENCZ",       0x7A, regMux },
    { "OUT8_CONN",       0x7B, regMux },
    /* Div blocks first pulse select */
    { "DIV_FIRST",       0x7C, regRW },
    /* Soft input register */
    { "SYS_RESET",       0x7E, regCmd },
    { "SOFT_IN",         0x7F, regRW },
    /* Position compare logic blocks */
    /* Load position counters */
    { "POS1_SETLO",      0x80, regCmd },
    { "POS1_SETHI",      0x81, regCmd },
    { "POS2_SETLO",      0x82, regCmd },
    { "POS2_SETHI",      0x83, regCmd },
    { "POS3_SETLO",      0x84, regCmd },
    { "POS3_SETHI",      0x85, regCmd },
    { "POS4_SETLO",      0x86, regCmd },
    { "POS4_SETHI",      0x87, regCmd },
    /* Select position counter 1,2,3,4,Sum */
    { "PC_ENC",          0x88, regRW },
    /* Timestamp clock prescaler */
    { "PC_TSPRE",        0x89, regRW },
    /* Arm input Soft,External */
    { "PC_ARM_SEL",      0x8A, regRW },
    /* Soft arm and disarm commands */
    { "PC_ARM",          0x8B, regCmd },
    { "PC_DISARM",       0x8C, regCmd },
    /* Gate input Position,Time,External */
    { "PC_GATE_SEL",     0x8D, regRW },
    /* Gate parameters */
    { "PC_GATE_STARTLO", 0x8E, regRW },
    { "PC_GATE_STARTHI", 0x8F, regRW },
    { "PC_GATE_WIDLO",   0x90, regRW },
    { "PC_GATE_WIDHI",   0x91, regRW },
    { "PC_GATE_NGATELO", 0x92, regRW },
    { "PC_GATE_NGATEHI", 0x93, regRW },
    { "PC_GATE_STEPLO",  0x94, regRW },
    { "PC_GATE_STEPHI",  0x95, regRW },
    /* Pulse input Position,Time,External */
    { "PC_PULSE_SEL",    0x96, regRW },
    /* Pulse parameters */
    { "PC_PULSE_STARTLO",0x97, regRW },
    { "PC_PULSE_STARTHI",0x98, regRW },
    { "PC_PULSE_WIDLO",  0x99, regRW },
    { "PC_PULSE_WIDHI",  0x9A, regRW },
    { "PC_PULSE_STEPLO", 0x9B, regRW },
    { "PC_PULSE_STEPHI", 0x9C, regRW },
    { "PC_PULSE_MAXLO",  0x9D, regRW },
    { "PC_PULSE_MAXHI",  0x9E, regRW },
    /* PC_BIT_CAP moved to top of list so it is polled first */
    { "PC_DIR",          0xA0, regRW },
    { "PC_PULSE_DLYLO",  0xA1, regRW },
    { "PC_PULSE_DLYHI",  0xA2, regRW },
    /* System version */
    { "SYS_VER",         0xF0, regRO },
    /* SYS_STATE_ERR .. PC_NUM_CAPLO moved to end so they are polled quickly */
    { "PC_NUM_CAPHI",    0xF7, regRO },

    /*
     * Status values we should poll: FASTREGS
     */
    { "SYS_STATERR",     0xF1, regRO },
    { "SYS_STAT1LO",     0xF2, regRO },
    { "SYS_STAT1HI",     0xF3, regRO },
    { "SYS_STAT2LO",     0xF4, regRO },
    { "SYS_STAT2HI",     0xF5, regRO },
    { "PC_NUM_CAPLO",    0xF6, regRO },
};


/* These are the entries on the system bus */
static const char *bus_lookup[] = {
    "DISCONNECT",
    "IN1_TTL",
    "IN1_NIM",
    "IN1_LVDS",
    "IN2_TTL",
    "IN2_NIM",
    "IN2_LVDS",
    "IN3_TTL",
    "IN3_OC",
    "IN3_LVDS",
    "IN4_TTL",
    "IN4_CMP",
    "IN4_PECL",
    "IN5_ENCA",
    "IN5_ENCB",
    "IN5_ENCZ",
    "IN5_CONN",
    "IN6_ENCA",
    "IN6_ENCB",
    "IN6_ENCZ",
    "IN6_CONN",
    "IN7_ENCA",
    "IN7_ENCB",
    "IN7_ENCZ",
    "IN7_CONN",
    "IN8_ENCA",
    "IN8_ENCB",
    "IN8_ENCZ",
    "IN8_CONN",
    "PC_ARM",
    "PC_GATE",
    "PC_PULSE",
    "AND1",
    "AND2",
    "AND3",
    "AND4",
    "OR1",
    "OR2",
    "OR3",
    "OR4",
    "GATE1",
    "GATE2",
    "GATE3",
    "GATE4",
    "DIV1_OUTD",
    "DIV2_OUTD",
    "DIV3_OUTD",
    "DIV4_OUTD",
    "DIV1_OUTN",
    "DIV2_OUTN",
    "DIV3_OUTN",
    "DIV4_OUTN",
    "PULSE1",
    "PULSE2",
    "PULSE3",
    "PULSE4",
    "QUAD_OUTA",
    "QUAD_OUTB",
    "CLOCK_1KHZ",
    "CLOCK_1MHZ",
    "SOFT_IN1",
    "SOFT_IN2",
    "SOFT_IN3",
    "SOFT_IN4",
};




#endif
