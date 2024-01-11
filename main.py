import colorsys
import re
from typing import Tuple, cast

from bs4 import BeautifulSoup, Tag

cpp_colors = """
const FColor FColorList::White            ( 255, 255, 255, 255 );
const FColor FColorList::Red              ( 255,   0,   0, 255 );
const FColor FColorList::Green            (   0, 255,   0, 255 );
const FColor FColorList::Blue             (   0,   0, 255, 255 );
const FColor FColorList::Magenta          ( 255,   0, 255, 255 );
const FColor FColorList::Cyan             (   0, 255, 255, 255 );
const FColor FColorList::Yellow           ( 255, 255,   0, 255 );
const FColor FColorList::Black            (   0,   0,   0, 255 );
const FColor FColorList::Aquamarine       ( 112, 219, 147, 255 );
const FColor FColorList::BakerChocolate   (  92,  51,  23, 255 );
const FColor FColorList::BlueViolet       ( 159,  95, 159, 255 );
const FColor FColorList::Brass            ( 181, 166,  66, 255 );
const FColor FColorList::BrightGold       ( 217, 217,  25, 255 );
const FColor FColorList::Brown            ( 166,  42,  42, 255 );
const FColor FColorList::Bronze           ( 140, 120,  83, 255 );
const FColor FColorList::BronzeII         ( 166, 125,  61, 255 );
const FColor FColorList::CadetBlue        (  95, 159, 159, 255 );
const FColor FColorList::CoolCopper       ( 217, 135,  25, 255 );
const FColor FColorList::Copper           ( 184, 115,  51, 255 );
const FColor FColorList::Coral            ( 255, 127,   0, 255 );
const FColor FColorList::CornFlowerBlue   (  66,  66, 111, 255 );
const FColor FColorList::DarkBrown        (  92,  64,  51, 255 );
const FColor FColorList::DarkGreen        (  47,  79,  47, 255 );
const FColor FColorList::DarkGreenCopper  (  74, 118, 110, 255 );
const FColor FColorList::DarkOliveGreen   (  79,  79,  47, 255 );
const FColor FColorList::DarkOrchid       ( 153,  50, 205, 255 );
const FColor FColorList::DarkPurple       ( 135,  31, 120, 255 );
const FColor FColorList::DarkSlateBlue    ( 107,  35, 142, 255 );
const FColor FColorList::DarkSlateGrey    (  47,  79,  79, 255 );
const FColor FColorList::DarkTan          ( 151, 105,  79, 255 );
const FColor FColorList::DarkTurquoise    ( 112, 147, 219, 255 );
const FColor FColorList::DarkWood         ( 133,  94,  66, 255 );
const FColor FColorList::DimGrey          (  84,  84,  84, 255 );
const FColor FColorList::DustyRose        ( 133,  99,  99, 255 );
const FColor FColorList::Feldspar         ( 209, 146, 117, 255 );
const FColor FColorList::Firebrick        ( 142,  35,  35, 255 );
const FColor FColorList::ForestGreen      (  35, 142,  35, 255 );
const FColor FColorList::Gold             ( 205, 127,  50, 255 );
const FColor FColorList::Goldenrod        ( 219, 219, 112, 255 );
const FColor FColorList::Grey             ( 192, 192, 192, 255 );
const FColor FColorList::GreenCopper      (  82, 127, 118, 255 );
const FColor FColorList::GreenYellow      ( 147, 219, 112, 255 );
const FColor FColorList::HunterGreen      (  33,  94,  33, 255 );
const FColor FColorList::IndianRed        (  78,  47,  47, 255 );
const FColor FColorList::Khaki            ( 159, 159,  95, 255 );
const FColor FColorList::LightBlue        ( 192, 217, 217, 255 );
const FColor FColorList::LightGrey        ( 168, 168, 168, 255 );
const FColor FColorList::LightSteelBlue   ( 143, 143, 189, 255 );
const FColor FColorList::LightWood        ( 233, 194, 166, 255 );
const FColor FColorList::LimeGreen        (  50, 205,  50, 255 );
const FColor FColorList::MandarianOrange  ( 228, 120,  51, 255 );
const FColor FColorList::Maroon           ( 142,  35, 107, 255 );
const FColor FColorList::MediumAquamarine (  50, 205, 153, 255 );
const FColor FColorList::MediumBlue       (  50,  50, 205, 255 );
const FColor FColorList::MediumForestGreen( 107, 142,  35, 255 );
const FColor FColorList::MediumGoldenrod  ( 234, 234, 174, 255 );
const FColor FColorList::MediumOrchid     ( 147, 112, 219, 255 );
const FColor FColorList::MediumSeaGreen   (  66, 111,  66, 255 );
const FColor FColorList::MediumSlateBlue  ( 127,   0, 255, 255 );
const FColor FColorList::MediumSpringGreen( 127, 255,   0, 255 );
const FColor FColorList::MediumTurquoise  ( 112, 219, 219, 255 );
const FColor FColorList::MediumVioletRed  ( 219, 112, 147, 255 );
const FColor FColorList::MediumWood       ( 166, 128, 100, 255 );
const FColor FColorList::MidnightBlue     (  47,  47,  79, 255 );
const FColor FColorList::NavyBlue         (  35,  35, 142, 255 );
const FColor FColorList::NeonBlue         (  77,  77, 255, 255 );
const FColor FColorList::NeonPink         ( 255, 110, 199, 255 );
const FColor FColorList::NewMidnightBlue  (   0,   0, 156, 255 );
const FColor FColorList::NewTan           ( 235, 199, 158, 255 );
const FColor FColorList::OldGold          ( 207, 181,  59, 255 );
const FColor FColorList::Orange           ( 255, 127,   0, 255 );
const FColor FColorList::OrangeRed        ( 255,  36,   0, 255 );
const FColor FColorList::Orchid           ( 219, 112, 219, 255 );
const FColor FColorList::PaleGreen        ( 143, 188, 143, 255 );
const FColor FColorList::Pink             ( 188, 143, 143, 255 );
const FColor FColorList::Plum             ( 234, 173, 234, 255 );
const FColor FColorList::Quartz           ( 217, 217, 243, 255 );
const FColor FColorList::RichBlue         (  89,  89, 171, 255 );
const FColor FColorList::Salmon           ( 111,  66,  66, 255 );
const FColor FColorList::Scarlet          ( 140,  23,  23, 255 );
const FColor FColorList::SeaGreen         (  35, 142, 104, 255 );
const FColor FColorList::SemiSweetChocolate(107,  66,  38, 255 );
const FColor FColorList::Sienna           ( 142, 107,  35, 255 );
const FColor FColorList::Silver           ( 230, 232, 250, 255 );
const FColor FColorList::SkyBlue          (  50, 153, 204, 255 );
const FColor FColorList::SlateBlue        (   0, 127, 255, 255 );
const FColor FColorList::SpicyPink        ( 255,  28, 174, 255 );
const FColor FColorList::SpringGreen      (   0, 255, 127, 255 );
const FColor FColorList::SteelBlue        (  35, 107, 142, 255 );
const FColor FColorList::SummerSky        (  56, 176, 222, 255 );
const FColor FColorList::Tan              ( 219, 147, 112, 255 );
const FColor FColorList::Thistle          ( 216, 191, 216, 255 );
const FColor FColorList::Turquoise        ( 173, 234, 234, 255 );
const FColor FColorList::VeryDarkBrown    (  92,  64,  51, 255 );
const FColor FColorList::VeryLightGrey    ( 205, 205, 205, 255 );
const FColor FColorList::Violet           (  79,  47,  79, 255 );
const FColor FColorList::VioletRed        ( 204,  50, 153, 255 );
const FColor FColorList::Wheat            ( 216, 216, 191, 255 );
const FColor FColorList::YellowGreen      ( 153, 204,  50, 255 );
"""


def main() -> None:
    color_pattern = re.compile(
        r"FColorList::(\w+)\s+\(\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\s*\);"
    )
    matches = color_pattern.findall(cpp_colors)

    def rgba_to_hex(r: int, g: int, b: int) -> str:
        return f"{r:02X}{g:02X}{b:02X}"

    def rgba_to_hsva(
        r: int, g: int, b: int, a: int
    ) -> Tuple[float, float, float, float]:
        return colorsys.rgb_to_hsv(r / 255, g / 255, b / 255) + (a / 255,)

    soup = BeautifulSoup(
        "<html><head><title>Unreal Color Table</title></head><body></body></html>",
        "html.parser",
    )

    style_tag = soup.new_tag("style")
    style_tag.string = """
    body {
        background-color: #121212;
        color: #e0e0e0;
        font-family: sans-serif;
    }
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #333;
        padding: 5px;
        text-align: left;
    }
    .mono {
        font-family: monospace;
    }
    .color-preview {
        width: 100%;
    }
    .name-cell, .hex-cell {
        white-space: nowrap;
    }
    a:link, a:visited {
        color: #9ABCFF; /* Light blue color that works on dark backgrounds */
        text-decoration: none;
    }
    a:hover, a:active {
        color: #FFFFFF;
    }
    """
    cast(Tag, soup.head).append(style_tag)

    table = soup.new_tag("table")
    cast(Tag, soup.body).append(table)

    header_row = soup.new_tag("tr")
    table.append(header_row)

    headers = ["Name", "Hex Code", "Color Preview"]
    for header_name in headers:
        header = soup.new_tag("th")
        header.string = header_name
        header_row.append(header)

    # Sort colors by hue
    sorted_matches = sorted(
        matches, key=lambda x: rgba_to_hsva(int(x[1]), int(x[2]), int(x[3]), int(x[4]))
    )

    for name, r, g, b, _ in sorted_matches:
        hex_color = rgba_to_hex(int(r), int(g), int(b))
        row = soup.new_tag("tr")
        table.append(row)

        name_cell = soup.new_tag("td", attrs={"class": "mono name-cell"})
        name_cell.string = name
        row.append(name_cell)

        hex_cell = soup.new_tag("td", attrs={"class": "mono hex-cell"})
        hex_link = soup.new_tag(
            "a", href=f"https://www.htmlcsscolor.com/hex/{hex_color}", target="_blank"
        )
        hex_link.string = f"#{hex_color}"
        hex_cell.append(hex_link)
        row.append(hex_cell)

        color_cell = soup.new_tag(
            "td",
            attrs={"class": "color-preview"},
            style=f"background-color:#{hex_color};",
        )
        row.append(color_cell)

    html_page = soup.prettify()

    with open("index.html", "w") as file:
        file.write(html_page)


if __name__ == "__main__":
    main()
