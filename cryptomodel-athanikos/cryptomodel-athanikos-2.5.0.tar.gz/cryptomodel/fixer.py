from mongoengine import *


class Rates(EmbeddedDocument):
    meta = {'strict': False}
    AED = FloatField()
    AFN = FloatField()
    ALL = FloatField()
    AMD = FloatField()
    ANG = FloatField()
    AOA = FloatField()
    ARS = FloatField()
    AUD = FloatField()
    AWG = FloatField()
    AZN = FloatField()
    BAM = FloatField()
    BBD = FloatField()
    BDT = FloatField()
    BGN = FloatField()
    BHD = FloatField()
    BIF = FloatField()
    BMD = FloatField()
    BND = FloatField()
    BOB = FloatField()
    BRL = FloatField()
    BSD = FloatField()
    BTC = FloatField()
    BTN = FloatField()
    BWP = FloatField()
    BYN = FloatField()
    BYR = FloatField()
    BZD = FloatField()
    CAD = FloatField()
    CDF = FloatField()
    CHF = FloatField()
    CLF = FloatField()
    CLP = FloatField()
    CNY = FloatField()
    COP = FloatField()
    CRC = FloatField()
    CUC = FloatField()
    CUP = FloatField()
    CVE = FloatField()
    CZK = FloatField()
    DJF = FloatField()
    DKK = FloatField()
    DOP = FloatField()
    DZD = FloatField()
    EGP = FloatField()
    ERN = FloatField()
    ETB = FloatField()
    EUR = FloatField()
    FJD = FloatField()
    FKP = FloatField()
    GBP = FloatField()
    GEL = FloatField()
    GGP = FloatField()
    GHS = FloatField()
    GIP = FloatField()
    GMD = FloatField()
    GNF = FloatField()
    GTQ = FloatField()
    GYD = FloatField()
    HKD = FloatField()
    HNL = FloatField()
    HRK = FloatField()
    HTG = FloatField()
    HUF = FloatField()
    IDR = FloatField()
    ILS = FloatField()
    IMP = FloatField()
    INR = FloatField()
    IQD = FloatField()
    IRR = FloatField()
    ISK = FloatField()
    JEP = FloatField()
    JMD = FloatField()
    JOD = FloatField()
    JPY = FloatField()
    KES = FloatField()
    KGS = FloatField()
    KHR = FloatField()
    KMF = FloatField()
    KPW = FloatField()
    KRW = FloatField()
    KWD = FloatField()
    KYD = FloatField()
    KZT = FloatField()
    LAK = FloatField()
    LBP = FloatField()
    LKR = FloatField()
    LRD = FloatField()
    LSL = FloatField()
    LTL = FloatField()
    LVL = FloatField()
    LYD = FloatField()
    MAD = FloatField()
    MDL = FloatField()
    MGA = FloatField()
    MKD = FloatField()
    MMK = FloatField()
    MNT = FloatField()
    MOP = FloatField()
    MRO = FloatField()
    MUR = FloatField()
    MVR = FloatField()
    MWK = FloatField()
    MXN = FloatField()
    MYR = FloatField()
    MZN = FloatField()
    NAD = FloatField()
    NGN = FloatField()
    NIO = FloatField()
    NOK = FloatField()
    NPR = FloatField()
    NZD = FloatField()
    OMR = FloatField()
    PAB = FloatField()
    PEN = FloatField()
    PGK = FloatField()
    PHP = FloatField()
    PKR = FloatField()
    PLN = FloatField()
    PYG = FloatField()
    QAR = FloatField()
    RON = FloatField()
    RSD = FloatField()
    RUB = FloatField()
    RWF = FloatField()
    SAR = FloatField()
    SBD = FloatField()
    SCR = FloatField()
    SDG = FloatField()
    SEK = FloatField()
    SGD = FloatField()
    SHP = FloatField()
    SLL = FloatField()
    SOS = FloatField()
    SRD = FloatField()
    STD = FloatField()
    SVC = FloatField()
    SYP = FloatField()
    SZL = FloatField()
    THB = FloatField()
    TJS = FloatField()
    TMT = FloatField()
    TND = FloatField()
    TOP = FloatField()
    TRY = FloatField()
    TTD = FloatField()
    TWD = FloatField()
    TZS = FloatField()
    UAH = FloatField()
    UGX = FloatField()
    USD = FloatField()
    UYU = FloatField()
    UZS = FloatField()
    VEF = FloatField()
    VND = FloatField()
    VUV = FloatField()
    WST = FloatField()
    XAF = FloatField()
    XAG = FloatField()
    XAU = FloatField()
    XCD = FloatField()
    XDR = FloatField()
    XOF = FloatField()
    XPF = FloatField()
    YER = FloatField()
    ZAR = FloatField()
    ZMK = FloatField()
    ZMW = FloatField()
    ZWL = FloatField()


class exchange_rates(Document):
    meta = {'strict': False}
    _id = IntField(db_field='_id')
    success = BooleanField()
    base = StringField()
    rates = EmbeddedDocumentField(Rates, db_field='rates')
    date = StringField()
    timestamp = IntField()