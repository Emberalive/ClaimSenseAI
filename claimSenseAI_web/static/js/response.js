

window.addEventListener('load', () => {
    // Your Markdown content
    const markdown = document.getElementById("response_text");
    // Insert the HTML into the <p> tag
    document.getElementById("markdown-content").innerHTML = marked.parse(markdown)
})