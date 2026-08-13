async function generateVoice() {

    const brandInput = document.getElementById("brandInput");
    const tone = document.getElementById("tone").value;
    const audience = document.getElementById("audience").value;
    const resultCard = document.getElementById("resultCard");

    const description = brandInput.value.trim();

    if (!description) {
        resultCard.innerHTML = `
            <div class="result-empty">
                <div class="empty-icon">!</div>
                <h3>Please describe your brand</h3>
                <p>Enter some information about your brand first.</p>
            </div>
        `;
        return;
    }

    resultCard.innerHTML = `
        <div class="result-empty">
            <div class="empty-icon loading">✦</div>
            <h3>Creating your brand voice...</h3>
            <p>Analyzing your brand personality.</p>
        </div>
    `;

    try {

        const response = await fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                description: description,
                tone: tone,
                audience: audience
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Something went wrong."
            );
        }

        // Flask returns the generated data inside "result"
        const result = data.result || data;

        displayResult(result);

    } catch (error) {

        console.error(error);

        resultCard.innerHTML = `
            <div class="result-empty">

                <div class="empty-icon">
                    !
                </div>

                <h3>
                    Something went wrong
                </h3>

                <p>
                    ${escapeHTML(error.message)}
                </p>

            </div>
        `;
    }
}


function displayResult(data) {

    const resultCard =
        document.getElementById("resultCard");

    // Safely handle arrays
    const communication =
        Array.isArray(data.communication_style)
            ? data.communication_style
            : [];

    const wordsToUse =
        Array.isArray(data.words_to_use)
            ? data.words_to_use
            : [];

    const wordsToAvoid =
        Array.isArray(data.words_to_avoid)
            ? data.words_to_avoid
            : [];

    const examples =
        Array.isArray(data.example_messages)
            ? data.example_messages
            : [];

    window.generatedBrandVoice = {
        personality: data.personality || "",
        communication: communication,
        words_to_use: wordsToUse,
        words_to_avoid: wordsToAvoid,
        examples: examples
    };

    resultCard.innerHTML = `

        <div class="result-content">

            <div class="result-header">

                <div>

                    <span class="small-label">
                        ✦ GENERATED BRAND VOICE
                    </span>

                    <h2>
                        Your brand voice
                    </h2>

                </div>

                <button
                    class="copy-button"
                    onclick="copyResult()"
                >
                    Copy
                </button>

            </div>


            <div class="result-grid">


                <!-- PERSONALITY -->

                <div class="voice-box">

                    <div class="voice-icon">
                        ✦
                    </div>

                    <span class="box-label">
                        PERSONALITY
                    </span>

                    <p>
                        ${escapeHTML(data.personality || "Not available")}
                    </p>

                </div>


                <!-- COMMUNICATION -->

                <div class="voice-box">

                    <div class="voice-icon">
                        ◌
                    </div>

                    <span class="box-label">
                        COMMUNICATION STYLE
                    </span>

                    <ul>
                        ${communication.map(item => `
                            <li>
                                ${escapeHTML(item)}
                            </li>
                        `).join("")}
                    </ul>

                </div>


                <!-- WORDS TO USE -->

                <div class="voice-box">

                    <div class="voice-icon">
                        ✓
                    </div>

                    <span class="box-label">
                        WORDS TO USE
                    </span>

                    <ul>
                        ${wordsToUse.map(item => `
                            <li>
                                ${escapeHTML(item)}
                            </li>
                        `).join("")}
                    </ul>

                </div>


                <!-- WORDS TO AVOID -->

                <div class="voice-box">

                    <div class="voice-icon">
                        ×
                    </div>

                    <span class="box-label">
                        WORDS TO AVOID
                    </span>

                    <ul>
                        ${wordsToAvoid.map(item => `
                            <li>
                                ${escapeHTML(item)}
                            </li>
                        `).join("")}
                    </ul>

                </div>

            </div>


            <!-- EXAMPLES -->

            <div class="examples-box">

                <span class="box-label">
                    💬 EXAMPLE MESSAGES
                </span>

                <div class="examples">

                    ${examples.map((example, index) => `
                        <div class="example">
                            <strong>${index + 1}.</strong>
                            "${escapeHTML(example)}"
                        </div>
                    `).join("")}

                </div>

            </div>


        </div>
    `;
}


function escapeHTML(text) {

    const div = document.createElement("div");

    div.textContent = String(text);

    return div.innerHTML;
}


function copyResult() {

    const data = window.generatedBrandVoice;

    if (!data) {
        return;
    }

    const text = `

BRAND PERSONALITY

${data.personality}


COMMUNICATION STYLE

${data.communication.join("\n")}


WORDS TO USE

${data.words_to_use.join("\n")}


WORDS TO AVOID

${data.words_to_avoid.join("\n")}


EXAMPLE BRAND MESSAGES

${data.examples.join("\n")}

`;

    navigator.clipboard.writeText(text);

    const button =
        document.querySelector(".copy-button");

    if (button) {

        button.textContent = "Copied ✓";

        setTimeout(() => {
            button.textContent = "Copy";
        }, 2000);
    }
}


function scrollToGenerator() {

    const generator =
        document.getElementById("generator");

    if (generator) {

        generator.scrollIntoView({
            behavior: "smooth"
        });

    }
}


// Character counter

const brandInput =
    document.getElementById("brandInput");

const charCount =
    document.getElementById("charCount");


if (brandInput && charCount) {

    brandInput.addEventListener(
        "input",
        function () {

            if (this.value.length > 500) {

                this.value =
                    this.value.substring(0, 500);
            }

            charCount.textContent =
                this.value.length;

        }
    );
}