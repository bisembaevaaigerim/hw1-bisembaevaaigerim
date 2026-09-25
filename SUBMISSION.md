# HW1 submission

**Name:**
**Student ID:**
**Group:**
**Repository:**

## AI tool disclosure

State which AI tools you used and for what. Expected and fine; undisclosed use
is not.

> I used Claude and ChatGPT to understand the starter code provided by the teacher and to learn how to implement correctly the #TODO functions in registration_bot.py, correct_kazakh.py and tokenizer_forensics.py.
> I also used them to understand errors during the runs, such as the RateLimitError from OpenRouter.
> I ran all the scripts myself using my own API keys. All numbers in the tables come from my own runs and I wrote code and all the written answers myself based on my actual results.

---

## Sublab Easy — the registration bot and its bill

**How I laid the catalogue out inside the system prompt, and why:**

>I put the course catalogue into a simple bullet list, with one course on each line. Each line includes the course code, title, credits, prerequisites, schedule, available seats, total seats and instructor.
> I used plain text instead of JSON because the model needs to understand the information in natural language. For example, it needs to check time conflicts and add credits. A simple list is also easier for the model to read and use correctly.
> I divided the prompt into clear sections: RULES, STUDENT RECORD, CATALOGUE and HARD RULES. This makes the important rules easier to see and not hidden inside the course data.

**My turn 5 (Kazakh or Russian):**

> Мен үшінші курс студентімін. Маған тіркелуге әлі де болатын курстар қандай?

### Run 1 — OpenAI, `gpt-5.6-luna`

| Turn | Input tokens | Output tokens | Cost $ |
|---|---|---|---|
| 1 | 810 | 467 | 0.000722 |
| 2 | 1145 | 118 | 0.000371 |
| 3 | 1242 | 78 | 0.000342 |
| 4 | 1339 | 26 | 0.000299 |
| 5 | 1393 | 387 | 0.000743 |
| **total** | **6929** | **1076** | **0.002477** |

### Run 2 — OpenRouter, `deepseek/deepseek-v4-flash-0731:free`

| Turn | Input tokens | Output tokens | Cost $ |
|---|---|---|---|
| 1 | 888 | 3053 | 0.000000 |
| 2 | 1333 | 276 | 0.000000 |
| 3 | 1464 | 716 | 0.000000 |
| 4 | 1608 | 143 | 0.000000 |
| 5 | 1722 | 2040 | 0.000000 |
| **total** | **7015** | **6228** | **0.000000** |

### Turn 4, verbatim

The turn where you asked for CSS-4090, which does not exist. Paste both replies
exactly as they came back — do not tidy them.

**OpenAI:**

```
you: Add CSS-4090 Quantum Machine Learning to my schedule.
bot: I cannot add **CSS-4090 Quantum Machine Learning** because it does not exist in the provided course catalogue.
     in=  1339  out=   26  $0.000299

```

**OpenRouter:**

```
you: Add CSS-4090 Quantum Machine Learning to my schedule.
bot: I cannot add **CSS-4090 "Quantum Machine Learning"** because that course **does not exist in the catalogue** provided. I can only register courses from the catalogue, and CSS-4090 is not listed.

If you meant a course from the catalogue, please let me know which one, and I can check eligibility, seats, and scheduling for you.
     in=  1608  out=  143  $0.000000

```

### Written answers

**1. The two providers used almost identical code. What actually changed, and
what did not?**

> The API key and the base URL changed. The OpenAI client library, request format, message format and chat.completions.create() call remained the same.

**2. Why did the input token count climb on every turn when your questions
stayed roughly the same length? Use the numbers from your own table. What
happens to the bill at fifty turns?**

> The input token count increased on every turn because the whole conversation history was sent with each new question. The history included the system prompt, previous questions and previous answers.
> For OpenAI, the input tokens increased from 810 in turn 1 to 1393 in turn 5, which is 583 more tokens. For OpenRouter, they increased from 888 to 1722, which is 834 more tokens.
> At 50 turns, the input token count could become much larger. Based on the average growth in our first five turns, it could reach around 8000 tokens for OpenAI and around 11000 tokens for OpenRouter in a single request. The total bill would also increase because every request sends the full conversation history again. The exact cost depends on the length of the model's answers.

**3. Turn 4: did the bot refuse, or did it invent CSS-4090?** If it refused, what
in your system prompt held the line? If it invented, what did it make up —
credits, a room, an instructor?

> Both bots refused the request. GPT-5.6-luna gave a short answer and said that the course was not in the catalogue.
> DeepSeek also refused, but gave a longer explanation. It said that it can only register courses from the catalogue and offered to help with a real course.
> Neither bot made up credits, a classroom or a teacher for CSS-4090. I think this happened because of rule #1 in my system prompt. I clearly said that the catalogue is the only source of truth and that the model must refuse instead of making up a course. Both providers followed this rule.

**4. Where else was either bot wrong?** Turn 2 asks for two courses that meet at
the same hour; two courses in the catalogue are full. Did the bots notice?

> Both bots handled all the traps correctly. Both noticed the conflict between CSS-4007 and CSS-4102 on Tuesday from 09:00 to 10:50 in turn 1, and they mentioned it again in turns 2 and 3. Both refused to register both courses together and both correctly excluded CSS-4400 because it was full.
> Neither bot registered CSS-4090 in turn 4. I did not find any factual mistakes in either bot. The main difference was their style: DeepSeek gave longer answers, used tables and repeated the same calculations several times, while GPT was shorter and more direct. 
> DeepSeek also noticed that CSS-3011 had no free places, not only that the course had already been completed. GPT did not mention this.

---

## Sublab Medium — one task, six models

Paste the per-model summary printed by `correct_kazakh.py`:

| Model | Exact | Failed | Tokens | Cost $ |
|---|---|---|---|---|
| nex-n2.5-mini:free | 5 | 0 | 14140 | 0.00000 |
| laguna-s-2.1:free | 0 | 0 | 3708 | 0.00000 |
| nemotron-3-ultra-550b-a55b:free | 2 | 2 | 14026 | 0.00000 |
| gpt-5.6-luna | 6 | 0 | 3612 | 0.00336 |
| gpt-5.6-terra | 4 | 0 | 2829 | 0.02423 |
| gpt-5.6-sol | 7 | 0 | 2783 | 0.05919 |
### Which error types did each model repair?

Rows are error labels, columns are models. Write "yes", "no" or "partial".

| Error type | nex-n2.5-mini | laguna-s-2.1 | nemotron-3-ultra | luna | terra | sol |
|---|---|---|---|---|---|---|
| kaz_to_rus | partial | no | no | yes | partial | yes |
| latin_homoglyph | yes | no | partial | yes | partial | yes |
| drop_hyphen | yes | no | no | yes | yes | yes |
| join_words | yes | no | partial | yes | yes | yes |
| double_letter | yes | no | partial | yes | yes | yes |

**The `latin_homoglyph` row: what happened?** Describe what you observed. The
explanation is Sublab Harder's job, not this one's.

> Among the three OpenAI models, two (luna and sol) corrected both phrases containing Latin homoglyphs (KZ-03 and KZ-08), matching the original exactly. Terra corrected KZ-08 accurately but added extra punctuation marks (a comma and a question mark) in KZ-03, although the substitution of Latin letters with Cyrillic ones was performed correctly in all instances.
> Among the three openrouter models, the results were more mixed. `nex-n2.5-mini` corrected the Latin letters correctly in both sentences, but also added a comma and a question mark in KZ-03, the same pattern as terra. `nemotron-3-ultra` found the right letters to fix in both sentences, but each time it also changed something else that was not part of the corruption (it dropped a letter in KZ-03 and changed a word in KZ-08), so the core substitution was right but the output was not clean. `laguna-s-2.1` was the weakest: in KZ-03 it produced a different, garbled word instead of fixing the Latin letters, and in KZ-08 it invented an extra syllable that was not in the original word at all.

**Where a model returned good Kazakh that was not identical to the original,
say so here.** Exact match is not correctness.

> KZ-04 (luna, terra, sol) and KZ-05 (luna, terra) - all needed letters and words were corrected correctly, but the question mark is missing at the end of the sentence, even though the sentence is a question.
> I consider this a good correction: the `char_diff` is only 1 in these cases, and the text is grammatically correct. It is only different in punctuation.
> `nex-n2.5-mini` on KZ-03 is another example: it fixed all three Latin letters correctly and only added a comma and a question mark that were not in the original. The `char_diff` is 17 because of this punctuation, but the actual correction (fixing the homoglyphs) was done right.

**Cheapest model that was good enough, and why:**

> Among the three OpenAI models, the cheapest one is `gpt-5.6-luna` ($0.00336 for all 8 sentences). It gave 6/8 exact matches, which is almost the same as the most expensive model, `gpt-5.6-sol` (7/8 for $0.05919, about 17 times more expensive).


---

## Sublab Harder — open the tokenizer

### A. What a language costs

**`cl100k_base`:**

| Language | Tokens | Chars | Tok/char | × English | $ per 1,000 sentences |
|---|---|---|---|---|---|
| kk | 200 | 263 | 0.760 | 3.75x | $0.1666 |
| ru | 129 | 277 | 0.466 | 2.30x | $0.1076 |
| en | 59 | 291 | 0.203 | 1.00 | $0.0492 |

**`o200k_base`:**

| Language | Tokens | Chars | Tok/char | × English | $ per 1,000 sentences |
|---|---|---|---|---|---|
| kk | 84 | 263 | 0.319 | 1.58x | $0.0699 |
| ru | 74 | 277 | 0.267 | 1.32x | $0.0616 |
| en | 59 | 291 | 0.203 | 1.00 | $0.0492 |

### B. What a homoglyph does

One row per `latin_homoglyph` sentence in the dataset. Paste the actual decoded
token strings around the divergence point, not a description of them.

| Sentence id | Foreign char (index, name) | Tokens correct | Tokens corrupted | Δ | Diverges at |
|---|---|---|---|---|---|
| KZ-03 | 'A' (0, LATIN CAPITAL LETTER A); 'a' (2, LATIN SMALL LETTER A); 't' (5, LATIN SMALL LETTER T) | 16 | 20 | +4 | index 0 |
| KZ-08 | 'o' (1, LATIN SMALL LETTER O); 'a' (3, LATIN SMALL LETTER A); 'T' (9, LATIN CAPITAL LETTER T) | 21 | 24 | +3 | index 1 |

**Token pieces around the divergence:**

```
KZ-03
correct : ['А', 'лая', 'қ', 'тарға', ' ақша']
corrupted: ['A', 'л', 'a', 'я', 'қ']

KZ-08
correct : ['Д', 'он', 'аль', 'д', ' Т', 'рамп']
corrupted: ['Д', 'o', 'н', 'a', 'л', 'ль']
```

### C. Did it get better?

| Language | cl100k_base | o200k_base | Change |
|---|---|---|---|
| kk | 0.760 | 0.319 | −0.441 (−58%) |
| ru | 0.466 | 0.267 | −0.199 (−43%) |
| en | 0.203 | 0.203 | 0 (0%) |

### Written answers

**1. What is the Kazakh tax?** The ratio against English in both encodings, the
dollar figure from A, and how much it changed between the two tokenizers.

> In cl100k_base, Kazakh uses about 3.75 times more tokens than English. This means 1000 sentences cost about $0.1666 in Kazakh compared to $0.0492 in English, so Kazakh is about 3.4 times more expensive.
> In o200k_base, the difference is smaller. Kazakh uses about 1.58 times more tokens than English. The cost is $0.0699 for Kazakh and $0.0492 for English, so Kazakh is about 1.4 times more expensive.
> The newer tokenizer improved Kazakh a lot: the tokens-per-character ratio dropped by 58% (from 0.760 to 0.319). However, Kazakh still uses more tokens than English, so it is still more expensive for the same text.

**2. Why did the models repair `kaz_to_rus` but struggle with
`latin_homoglyph`?** Both are single-letter substitutions and both look almost
identical on screen. Use your token streams from B as the evidence. Say what the
model actually received in each case.

> In kaz_to_rus, one Cyrillic letter is replaced with another Cyrillic letter. The word still uses characters that the tokenizer often saw during training, so it can usually still recognize the word.
> In latin_homoglyph, a Cyrillic letter is replaced with a Latin letter that looks the same but is actually a different Unicode character. Because of this, the tokenizer may not recognize the word as one normal word.
> My token results show this clearly. In KZ-03, the correct word "Алаяқтарға" is split into larger parts: ['А', 'лая', 'қ', 'тарға', ...]. The tokenizer recognizes it as a real word.
> But the corrupted version, with Latin A, a, and t, is split into single characters: ['A', 'л', 'a', 'я', 'қ']. The token count increases by 4 (from 16 to 20), even though only 3 characters were changed. This happens because the tokenizer no longer recognizes the word as a normal word.
> KZ-08 shows the same pattern. "Дональд" is normally split as ['Д', 'он', 'аль', 'д']. But when it is changed to "Дoнaльд", it is split into ['Д', 'o', 'н', 'a', 'л', 'ль']. The word breaks apart exactly where the Latin letters appear.
 
**3. Name one thing this measurement does not explain about your Sublab Medium
results.** You measured OpenAI's tokenizers; three of your six models were not
OpenAI's. What follows, and what would you have to do to close the gap?

> I only measured two OpenAI tokenizers, cl100k_base and o200k_base. But three of my six Sublab Medium models were not from OpenAI: nex-n2.5-mini, laguna-s-2.1 and nemotron-3-ultra all came through OpenRouter and almost certainly use their own tokenizers with different vocabularies.
> So this measurement can explain the latin_homoglyph pattern for gpt-5.6-luna, gpt-5.6-terra and gpt-5.6-sol, but it does not tell me why laguna-s-2.1 performed so poorly on the whole task (0/8 exact matches) or why nemotron-3-ultra failed outright on two sentences. Those failures might not be about tokenization at all - laguna-s-2.1 is a coding-focused model, so it may simply not be trained well for natural language correction tasks, regardless of how its tokenizer splits the text.
> To close this gap, I would need to find and load each model's own tokenizer (if it is publicly available) and repeat measurement B with it, instead of assuming that OpenAI's tokenizers represent all six models. I would also need a separate way to test whether a model's poor performance comes from tokenization or from the model itself not being suited for the task.
