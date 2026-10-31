//! tokens.rs -- généré par gen/gen_tokens.py (cdx-ui 1.0.0) depuis tokens.json : ne pas modifier à la main.
//! Couleurs au format 0xRRGGBB.
#![allow(dead_code)]

pub const FRAME: u32 = 0x222222;
pub const PANEL: u32 = 0x333333;
pub const BTN: u32 = 0x333333;
pub const CARD_2: u32 = 0x2A2A2A;
pub const INK: u32 = 0x000000;
pub const LINE: u32 = 0x555555;
pub const HI: u32 = 0x666666;
pub const LO: u32 = 0x000000;
pub const TEXT: u32 = 0xFFFFFF;
pub const MUTED: u32 = 0xFFFFFF;
pub const FAINT: u32 = 0x888888;
pub const ACCENT_2: u32 = 0xFFCC99;
pub const ROW_HOVER: u32 = 0x3A3A3A;
pub const ROW_SEL: u32 = 0x3F3F3F;
pub const ROW_SEL_RING: u32 = 0x777777;
pub const GREEN: u32 = 0x00FF00;
pub const WARN: u32 = 0xFAA320;
pub const RED: u32 = 0xFF5A4A;

pub struct Accent {
    pub id: &'static str,
    pub edge: u32,
    pub mid: u32,
    pub dark: u32,
    pub hover: u32,
    pub title_from: u32,
    pub title_to: u32,
    pub bar_top: u32,
    pub bar_mid: u32,
    pub bar_bot: u32,
    pub spark: u32,
    pub accent: u32,
    pub field_ink: u32,
    pub sel_bg: u32,
    pub sel_fg: u32,
    pub icon_accent: u32,
    pub icon_accent_dark: u32,
}

/// `ACCENTS[0]` est le défaut (rouge CDX).
pub const ACCENTS: [Accent; 7] = [
    Accent { id: "rouge", edge: 0xCC0000, mid: 0x880000, dark: 0x440000, hover: 0x660000, title_from: 0x320000, title_to: 0xC30000, bar_top: 0xE83C3C, bar_mid: 0xC01010, bar_bot: 0x8A0202, spark: 0xFF8A74, accent: 0xD41818, field_ink: 0x00FF00, sel_bg: 0x001177, sel_fg: 0xFF00FF, icon_accent: 0xE02020, icon_accent_dark: 0x8A0202 },
    Accent { id: "bleu", edge: 0x0000FF, mid: 0x0000AA, dark: 0x000055, hover: 0x000080, title_from: 0x00003E, title_to: 0x0000F4, bar_top: 0x4242FF, bar_mid: 0x1313EF, bar_bot: 0x0202AC, spark: 0x7373FF, accent: 0x1C1CFF, field_ink: 0x8FD0FF, sel_bg: 0x001177, sel_fg: 0xFF00FF, icon_accent: 0x1313EF, icon_accent_dark: 0x0202AC },
    Accent { id: "vert", edge: 0x00CC00, mid: 0x008800, dark: 0x004400, hover: 0x006600, title_from: 0x003200, title_to: 0x00C300, bar_top: 0x3CE83C, bar_mid: 0x0FBF0F, bar_bot: 0x018A01, spark: 0x73FF73, accent: 0x17D417, field_ink: 0x00FF00, sel_bg: 0x004422, sel_fg: 0xFFFF00, icon_accent: 0x0FBF0F, icon_accent_dark: 0x018A01 },
    Accent { id: "violet", edge: 0xE000E0, mid: 0x960096, dark: 0x4B004B, hover: 0x700070, title_from: 0x370037, title_to: 0xD700D7, bar_top: 0xFF42FF, bar_mid: 0xD211D2, bar_bot: 0x970297, spark: 0xFF73FF, accent: 0xE91AE9, field_ink: 0xFFA8FF, sel_bg: 0x2A0044, sel_fg: 0x00FFFF, icon_accent: 0xD211D2, icon_accent_dark: 0x970297 },
    Accent { id: "ambre", edge: 0xCC4704, mid: 0x882F03, dark: 0x441801, hover: 0x662302, title_from: 0x321101, title_to: 0xC34404, bar_top: 0xE87840, bar_mid: 0xBF4C13, bar_bot: 0x8A3104, spark: 0xFFA376, accent: 0xD4591B, field_ink: 0xFFB04A, sel_bg: 0x3A1800, sel_fg: 0xFFE090, icon_accent: 0xBF4C13, icon_accent_dark: 0x8A3104 },
    Accent { id: "sarcelle", edge: 0x75EBEB, mid: 0x4E9C9C, dark: 0x274E4E, hover: 0x3B7575, title_from: 0x1D3939, title_to: 0x70E0E0, bar_top: 0xA1FFFF, bar_mid: 0x77DCDC, bar_bot: 0x509E9E, spark: 0xB9FFFF, accent: 0x87F3F3, field_ink: 0xA8FFF0, sel_bg: 0x003A3A, sel_fg: 0xFFFFFF, icon_accent: 0x77DCDC, icon_accent_dark: 0x509E9E },
    Accent { id: "charbon", edge: 0xCCCCCC, mid: 0x888888, dark: 0x444444, hover: 0x666666, title_from: 0x323232, title_to: 0xC3C3C3, bar_top: 0xE8E8E8, bar_mid: 0xBFBFBF, bar_bot: 0x8A8A8A, spark: 0xFFFFFF, accent: 0xD4D4D4, field_ink: 0xE6E6E6, sel_bg: 0x444444, sel_fg: 0xFFFFFF, icon_accent: 0xBFBFBF, icon_accent_dark: 0x8A8A8A },
];

pub const TEXT_SIZE: i32 = 14;
pub const LINE_HEIGHT: i32 = 16;
pub const LOG_LINE_HEIGHT: i32 = 13;
pub const TITLE_HEIGHT: i32 = 21;
pub const FRAME_RING: i32 = 5;
pub const FRAME_OUTLINE: i32 = 1;
pub const TITLE_BUTTON_SIZE: i32 = 14;
pub const SCROLLBAR_SIZE: i32 = 15;
pub const CONTROL_HEIGHT: i32 = 20;
pub const BAR_BUTTON_HEIGHT: i32 = 22;
pub const COLUMN_HEADER_HEIGHT: i32 = 22;
pub const CHECKBOX_SIZE: i32 = 14;
pub const ICON_SIZE: i32 = 16;
pub const SNAP_DISTANCE: i32 = 10;
pub const SNAP_GAP: i32 = 2;
