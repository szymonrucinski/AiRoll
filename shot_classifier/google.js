urls = Array.from(document.querySelectorAll(".rg_i")).map((el) =>
  el.hasAttribute("data-src")
    ? el.getAttribute("data-src")
    : el.getAttribute("data-iurl")
);
window.open("data:text/csv;charset=utf-8," + escape(urls.join("\n")));
