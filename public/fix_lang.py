import os
import re
from bs4 import BeautifulSoup

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    changed = False

    # Force html tag lang="ja" and remove lang classes
    html_tag = soup.find('html')
    if html_tag:
        if html_tag.get('lang') != 'ja':
            html_tag['lang'] = 'ja'
            changed = True
        classes = html_tag.get('class', [])
        if 'lang-pending' in classes:
            classes.remove('lang-pending')
            changed = True
        if 'lang-ja' in classes:
            classes.remove('lang-ja')
            changed = True
        if not classes and html_tag.get('class'):
            del html_tag['class']
            changed = True

    # 1. Decompose tags with lang="en"
    for tag in soup.find_all(attrs={'lang': 'en'}):
        tag.decompose()
        changed = True

    # 2. For tags with lang="ja", remove the attribute and unwrap if it's an empty span
    for tag in soup.find_all(attrs={'lang': 'ja'}):
        del tag['lang']
        if tag.name == 'span' and not tag.attrs:
            tag.unwrap()
        changed = True

    # 3. Remove language switcher components
    for tag in soup.find_all(class_='language-switcher'):
        tag.decompose()
        changed = True
    for tag in soup.find_all(class_='global-language-switcher'):
        tag.decompose()
        changed = True
    for label in soup.find_all('label', attrs={'for': 'language-select'}):
        label.decompose()
        changed = True

    # 4. Remove scripts related to language switching
    for script in soup.find_all('script'):
        if script.string:
            s_content = script.string
            if 'face-score-language' in s_content or 'language-select' in s_content or 'lang-pending' in s_content:
                script.decompose()
                changed = True
            elif 'document.documentElement.lang=' in s_content and 'face-score-global-language' in s_content:
                # Also likely a language initialisation block
                script.decompose()
                changed = True

    # 5. Remove css styles related to language
    for style in soup.find_all('style'):
        if style.string:
            s_content = style.string
            if 'lang-pending' in s_content or 'language-switcher' in s_content:
                new_styles = re.sub(r'html\.lang-pending[^}]*\}', '', s_content, flags=re.DOTALL)
                new_styles = re.sub(r'html:not\(\.lang-ja\)\s*\[lang="ja"\]\s*\{[^}]*\}', '', new_styles, flags=re.DOTALL)
                new_styles = re.sub(r'html\.lang-ja\s*\[lang="en"\]\s*\{[^}]*\}', '', new_styles, flags=re.DOTALL)
                new_styles = re.sub(r'\.language-switcher\s*\{[^}]*\}', '', new_styles, flags=re.DOTALL)
                new_styles = re.sub(r'\.language-switcher\s+select\s*\{[^}]*\}', '', new_styles, flags=re.DOTALL)
                new_styles = re.sub(r'@media[^{]*\{\s*\.language-switcher\s*\{[^}]*\}\s*\}', '', new_styles, flags=re.DOTALL)
                if new_styles != s_content:
                    # In case the whole block is now practically empty, decompose it
                    if not new_styles.strip():
                        style.decompose()
                    else:
                        style.string.replace_with(new_styles)
                    changed = True

    # 6. Remove stray language separator slashes ' / '
    # We iterate over NavigableString
    for text_node in soup.find_all(string=True):
        if re.match(r'^\s*/\s*$', text_node):
            text_node.extract()
            changed = True

    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Processed: {file_path}")

directory = '.'
for root, dirs, files in os.walk(directory):
    for name in files:
        if name.endswith('.html'):
            process_file(os.path.join(root, name))
print("Done")
