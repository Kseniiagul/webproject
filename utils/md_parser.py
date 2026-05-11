import markdown

def to_html(text):
    if not text:
        return ''
    return markdown.markdown(text)

def to_txt(text):
    if not text:
        return ''
    result = text
    result = result.replace('#', '')
    result = result.replace('**', '')
    result = result.replace('*', '')
    result = result.replace('-', '')
    result = result.replace('`', '')
    result = result.replace('~~', '')
    result = result.replace('[', '')
    result = result.replace(']', '')
    result = result.replace('(', '')
    result = result.replace(')', '')

    lines = result.split('\n')
    clean_lines = [line.strip() for line in lines]

    return '\n'.join(clean_lines)
