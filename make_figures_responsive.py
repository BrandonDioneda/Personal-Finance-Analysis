"""
Run this script from the root of your Personal-Finance-Analysis repo.
It patches every Plotly HTML figure file to be responsive (fills its container).
No need to re-run your analysis — it edits the exported files in place.
"""

import os
import re

FIGURES_DIR = "figures"

# This is what Plotly writes for a fixed-size config
FIXED_PATTERN = re.compile(r'"responsive":\s*false', re.IGNORECASE)

# Patches Plotly used autosize behavior embedded in the HTML
AUTOSIZE_PATCH = """
<script>
  window.addEventListener('load', function () {
    var plots = document.querySelectorAll('.plotly-graph-div');
    plots.forEach(function (plot) {
      plot.style.width = '100%';
      plot.style.height = '100%';
      if (window.Plotly) {
        Plotly.relayout(plot, { autosize: true });
      }
    });
    document.documentElement.style.height = '100%';
    document.body.style.height = '100%';
    document.body.style.margin = '0';
  });
</script>
"""

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already patched
    if 'make_figures_responsive' in content:
        print(f"  Already patched: {filepath}")
        return

    # 1. Replace "responsive": false with "responsive": true
    content = FIXED_PATTERN.sub('"responsive": true', content)

    # 2. Inject our resize script just before </body>
    marker = '<!-- patched by make_figures_responsive -->'
    if '</body>' in content:
        content = content.replace('</body>', marker + AUTOSIZE_PATCH + '</body>')
    else:
        content += marker + AUTOSIZE_PATCH

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  Patched: {filepath}")


def main():
    patched = 0
    for root, dirs, files in os.walk(FIGURES_DIR):
        for fname in files:
            if fname.endswith('.html'):
                patch_file(os.path.join(root, fname))
                patched += 1
    print(f"\nDone. {patched} file(s) processed.")
    print("Now commit and push the figures/ folder to GitHub.")


if __name__ == '__main__':
    main()
