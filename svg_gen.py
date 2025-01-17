import svgwrite


def wrap_text(text, max_width, font_size):
    """按最大宽度自动换行"""
    words = text.split(" ")
    lines = []
    current_line = words[0]

    for word in words[1:]:
        if (
            len(current_line + " " + word) * font_size * 0.6 <= max_width
        ):  # 大致估算每个字符的宽度
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)  # 添加最后一行
    return lines


def main(references):
    # 创建 SVG 文件
    dwg = svgwrite.Drawing("reference_card.svg", size=("800px", "400px"))

    # 背景颜色
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="black"))

    # 插入图片（假设图片路径为 "bird.png"）
    dwg.add(dwg.image(href="bird.png", insert=(20, 100), size=(150, 150)))

    # 添加标题
    dwg.add(
        dwg.text(
            "REFERENCE",
            insert=(400, 50),
            fill="white",
            style="font-family:Alexandria Regular; font-size:30px; font-weight:bold;",
            text_anchor="middle",
        )
    )

    # 添加参考文献
    y_offset = 100
    line_height = 20
    font_size = 14
    max_width = 700  # 最大宽度限制

    for ref in references:
        lines = wrap_text(ref, max_width, font_size)
        for line in lines:
            dwg.add(
                dwg.text(
                    line,
                    insert=(200, y_offset),
                    fill="white",
                    style=f"font-family:Alexandria; font-size:{font_size}px;",
                    text_anchor="start",
                )
            )
            y_offset += line_height
        y_offset += 10  # 每个参考文献之间增加额外间距

    # 添加 @SCAI_Agent 下方文本
    dwg.add(
        dwg.text(
            "@SCAI_Agent",
            insert=(95, 270),  # 放在图片下方
            fill="white",
            style="font-family:Courier New; font-size:14px; font-weight:bold;",
            text_anchor="middle",
        )
    )

    # 添加下方描述文字
    description = "Multiple agents in SCAI collaborate to ensure reliable, evidence-based answers through literature search and analysis."
    lines = wrap_text(description, 600, font_size)
    y_offset = 320
    for line in lines:
        dwg.add(
            dwg.text(
                line,
                insert=(200, y_offset),
                fill="white",
                style=f"font-family:Courier New; font-size:{font_size}px;",
            )
        )
        y_offset += line_height

    # 保存 SVG
    dwg.save()


main(
    [
        "1. Vaswani, A. (2017). Attention is all you need. Advances in Neural Information Processing Systems.",
        "2. Bahdanau, D. (2014). Neural machine translation by jointly learning to align and translate. arXiv preprint arXiv:1409.0473.",
        "3. Luong, M. T. (2015). Effective approaches to attention-based neural machine translation. arXiv preprint arXiv:1508.04025.",
    ]
)
