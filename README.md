# LLM Quiz Time

![Deploy](https://github.com/kaustubhdhole/llm-quiz-time/actions/workflows/deploy.yml/badge.svg)
![License](https://img.shields.io/github/license/llmquiz/llm-quiz-time)
![Issues](https://img.shields.io/github/issues/llmquiz/llm-quiz-time)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Fkaustubhdhole.github.io%2Fllm-quiz-time%2F)](https://kaustubhdhole.github.io/llm-quiz-time/)

```
-+-+-+ +-+-+-+-+ +-+-+-+-+
|L|L|M| |Q|u|i|z| |T|i|m|e|
-+-+-+ +-+-+-+-+ +-+-+-+-+
```

A simple web-based quiz app that shows a random question on each refresh.
Topics now include planning, reasoning, long-context, data valuation, learning rates, and tokenization.

## Usage
Open `index.html` in your browser. The page fetches questions from
`questions.json` and displays one randomly.

## Deployment
The repository includes a GitHub Actions workflow that publishes the contents of
the `main` branch to GitHub Pages. Because this repository is not named
`llmquiz.github.io`, the site is served from the repository subpath. After
pushing to `main`, the website will be available at
[https://kaustubhdhole.github.io/llm-quiz-time/](https://kaustubhdhole.github.io/llm-quiz-time/)
(note the trailing `/`).

If the page still returns a 404, verify that GitHub Pages is enabled for this
repository with **GitHub Actions** selected as the source. The `pages-build-deployment`
workflow must complete successfully before the site becomes accessible.
