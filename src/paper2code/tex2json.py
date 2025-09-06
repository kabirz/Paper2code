import re
import json

def parse_tex_section(buffer):
    pattern = r'(\\(?:sub)*section)\{([\s\S]*?)\}\s*\\label\{([\s\S]*?)\}\s*([\s\S]*?)(?=\\(?:sub)*section|\Z)'

    matches = re.findall(pattern, buffer, flags=re.DOTALL)

    results = []
    for sec_type, title, label, content in matches:
        results.append({
            "type": sec_type,       # \section 或 \subsection
            "title": title.strip(),
            "label": label.strip(),
            "content": content.strip()
        })
    return json.dumps(results, indent=2, ensure_ascii=False)
