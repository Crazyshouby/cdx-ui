// kdx-tokens.h -- généré par gen/gen_tokens.py (kdx-ui 1.0.0) depuis tokens.json : ne pas modifier à la main.
// Couleurs au format 0xRRGGBB. Pour un COLORREF Win32 (0x00BBGGRR) : kdx::Colorref(kdx::kFrame).
#pragma once

namespace kdx {

constexpr unsigned Colorref(unsigned rgb) { return ((rgb & 0xFFu) << 16) | (rgb & 0xFF00u) | ((rgb >> 16) & 0xFFu); }

constexpr unsigned kFrame = 0x222222;
constexpr unsigned kPanel = 0x333333;
constexpr unsigned kBtn = 0x333333;
constexpr unsigned kCard2 = 0x2A2A2A;
constexpr unsigned kInk = 0x000000;
constexpr unsigned kLine = 0x555555;
constexpr unsigned kHi = 0x666666;
constexpr unsigned kLo = 0x000000;
constexpr unsigned kText = 0xFFFFFF;
constexpr unsigned kMuted = 0xFFFFFF;
constexpr unsigned kFaint = 0x888888;
constexpr unsigned kAccent2 = 0xFFCC99;
constexpr unsigned kRowHover = 0x3A3A3A;
constexpr unsigned kRowSel = 0x3F3F3F;
constexpr unsigned kRowSelRing = 0x777777;
constexpr unsigned kGreen = 0x00FF00;
constexpr unsigned kWarn = 0xFAA320;
constexpr unsigned kRed = 0xFF5A4A;

struct Accent {
    const char* id;
    unsigned edge, mid, dark, hover, titleFrom, titleTo, barTop, barMid, barBot, spark, accent, fieldInk, selBg, selFg, iconAccent, iconAccentDark;
};

// kAccents[0] est le défaut (rouge KDX).
constexpr Accent kAccents[] = {
    {"rouge", 0xCC0000, 0x880000, 0x440000, 0x660000, 0x320000, 0xC30000, 0xE83C3C, 0xC01010, 0x8A0202, 0xFF8A74, 0xD41818, 0x00FF00, 0x001177, 0xFF00FF, 0xE02020, 0x8A0202},
    {"bleu", 0x0000FF, 0x0000AA, 0x000055, 0x000080, 0x00003E, 0x0000F4, 0x4242FF, 0x1313EF, 0x0202AC, 0x7373FF, 0x1C1CFF, 0x8FD0FF, 0x001177, 0xFF00FF, 0x1313EF, 0x0202AC},
    {"vert", 0x00CC00, 0x008800, 0x004400, 0x006600, 0x003200, 0x00C300, 0x3CE83C, 0x0FBF0F, 0x018A01, 0x73FF73, 0x17D417, 0x00FF00, 0x004422, 0xFFFF00, 0x0FBF0F, 0x018A01},
    {"violet", 0xE000E0, 0x960096, 0x4B004B, 0x700070, 0x370037, 0xD700D7, 0xFF42FF, 0xD211D2, 0x970297, 0xFF73FF, 0xE91AE9, 0xFFA8FF, 0x2A0044, 0x00FFFF, 0xD211D2, 0x970297},
    {"ambre", 0xCC4704, 0x882F03, 0x441801, 0x662302, 0x321101, 0xC34404, 0xE87840, 0xBF4C13, 0x8A3104, 0xFFA376, 0xD4591B, 0xFFB04A, 0x3A1800, 0xFFE090, 0xBF4C13, 0x8A3104},
    {"sarcelle", 0x75EBEB, 0x4E9C9C, 0x274E4E, 0x3B7575, 0x1D3939, 0x70E0E0, 0xA1FFFF, 0x77DCDC, 0x509E9E, 0xB9FFFF, 0x87F3F3, 0xA8FFF0, 0x003A3A, 0xFFFFFF, 0x77DCDC, 0x509E9E},
    {"charbon", 0xCCCCCC, 0x888888, 0x444444, 0x666666, 0x323232, 0xC3C3C3, 0xE8E8E8, 0xBFBFBF, 0x8A8A8A, 0xFFFFFF, 0xD4D4D4, 0xE6E6E6, 0x444444, 0xFFFFFF, 0xBFBFBF, 0x8A8A8A},
};
constexpr int kAccentCount = 7;

constexpr int kTextSize = 14;
constexpr int kLineHeight = 16;
constexpr int kLogLineHeight = 13;
constexpr int kTitleHeight = 21;
constexpr int kFrameRing = 5;
constexpr int kFrameOutline = 1;
constexpr int kTitleButtonSize = 14;
constexpr int kScrollbarSize = 15;
constexpr int kControlHeight = 20;
constexpr int kBarButtonHeight = 22;
constexpr int kColumnHeaderHeight = 22;
constexpr int kCheckboxSize = 14;
constexpr int kIconSize = 16;
constexpr int kSnapDistance = 10;
constexpr int kSnapGap = 2;

}  // namespace kdx
