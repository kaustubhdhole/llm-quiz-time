# LLM Quiz Time

[![Build](https://github.com/llmquiz/llm-quiz-time/actions/workflows/deploy.yml/badge.svg)](https://github.com/llmquiz/llm-quiz-time/actions/workflows/deploy.yml) [![License](https://img.shields.io/github/license/llmquiz/llm-quiz-time)](LICENSE) [![Open Issues](https://img.shields.io/github/issues/llmquiz/llm-quiz-time)](https://github.com/llmquiz/llm-quiz-time/issues) [![Website](https://img.shields.io/badge/website-live-brightgreen)](https://kaustubhdhole.github.io/llm-quiz-time/)

```text
-+-+-+ +-+-+-+-+ +-+-+-+-+
|L|L|M| |Q|u|i|z| |T|i|m|e|
-+-+-+ +-+-+-+-+ +-+-+-+-+
```

A simple web-based quiz app that shows a random question on each refresh.

## Usage
Open `index.html` in your browser. The page fetches questions from
`questions.json` and displays one randomly.

## Deployment
The repository includes a GitHub Actions workflow that publishes the contents of
the `main` branch to GitHub Pages. Because this repository is not named
`llmquiz.github.io`, the site is served from the repository subpath. After
pushing to `main`, the website will be available at
[https://llmquiz.github.io/llm-quiz-time/](https://llmquiz.github.io/llm-quiz-time/)
(note the trailing `/`).

If the page still returns a 404, verify that GitHub Pages is enabled for this
repository with **GitHub Actions** selected as the source. The `pages-build-deployment`
workflow must complete successfully before the site becomes accessible.
