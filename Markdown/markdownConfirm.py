import markdown2

test_markdown = """
# Title

This is a paragraph in Markdown.

## Subheading

- Bullet point 1
- Bullet point 2

[Link](http://example.com)

1. Testing: Here 
2. Testing2: Here 

1. Test
2. Test
"""

html = markdown2.markdown(test_markdown)
print("Generated HTML:")
print(html)
