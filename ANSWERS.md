1. Prediction:
    ru/en = 576/300 ~ 1.92x
    kk/en = 640/300 ~ 2.13x
  Real result:
    complaint      en=92 tokens  ru=134 tokens  kk=198 tokens
    ru/en = 134/92 ~ 1.46x
    kk/en = 198/92 ~ 2.15x

    The prediction is made by calculating bytes, as words and sentences are human based
    language and a machine considers everything as 0s and 1s, so in case of predictions
    the closest we can get is by taking bytes, especially when we know that a letter in
    Latin is only 1 byte, whereas Kazakh and Russian languages require 2 bytes per
    letter.

2.
    AT 5,000 REQUESTS/DAY -- US dollars per year
  ------------------------------------------------------------------------
                          EN          RU          KK
  haiku-4.5            8,212      12,217      12,240
  sonnet-5            16,425      24,433      24,481
  opus-5              41,062      61,083      61,201
  fable-5.1           82,125     122,166     122,403

  5000 is a large enough number to handle all user requests, as from personal experience
  people spend less than 5 questions to get a solution or answer, especially if we
  consider the fact that most problems are shared among many people and are easy to
  solve, and it allows us to handle 1000 users per day, which is a decent number for a
  bank.

3. The answer is between sonnet-5 and opus-5. Let's take sonnet-5, since more complex
  or risky requests, where any error can cost a high payment, are more likely to be
  escalated to a human assistant rather than handled by an LLM alone. That means the
  LLM mainly needs to be reliable on routine, everyday complaints, and sonnet-5 clears
  that bar without paying opus-5's price. Considering these factors, we can conclude
  that our option is suitable due to its not very high price, decent request
  processing, and low hallucination rate on understandable answers in Kazakh. We may
  also take into account that Kazakh requires more tokens than English, so the topic of
  price is really important.

4. Prompt caching, so you don't pay extra tokens for processing the same question over
  and over, while keeping the full prompt context "active" across requests. It also
  influences speed as we check if this or a similar question was already processed.

----- ADDITIONAL TASKS -----

1. NEW_PROMPT
  ------------------------------------------------------------------
                          EN           RU           KK
  o200k_base               30           41           54
    ÷ EN                1.00x        1.37x        1.80x
  cl100k_base              30           69          116
    ÷ EN                1.00x        2.30x        3.87x

The newly added texts are shorter and less complicated than complaint ones, by this
fact we can explain why numbers are a bit outside the band, but the meaning stays
almost the same.

2.
  FIRST_KK
  ------------------------------------------------------------------
                          EN           RU           KK
  chars                     9            6           60
  bytes                     9           11          111
  words                     1            1            8
  bytes/EN              1.00x        1.22x       12.33x
  bytes/char             1.00         1.83         1.85

  SECOND_KK
  ------------------------------------------------------------------
                          EN           RU           KK
  chars                     9            6           51
  bytes                     9           11           91
  words                     1            1           10
  bytes/EN              1.00x        1.22x       10.11x
  bytes/char             1.00         1.83         1.78

  FIRST_KK
------------------------------------------------------------------
                         EN           RU           KK
o200k_base                1            2           20
  ÷ EN                1.00x        2.00x       20.00x
cl100k_base               1            4           36
  ÷ EN                1.00x        4.00x       36.00x

SECOND_KK
------------------------------------------------------------------
                         EN           RU           KK
o200k_base                1            2           17
  ÷ EN                1.00x        2.00x       17.00x
cl100k_base               1            4           40
  ÷ EN                1.00x        4.00x       40.00x

It has to be taken into consideration that the length of the sentences is similar but
not the same, however it anyway shows that cl100k spends more tokens, and as a result
more money, to process special Kazakh letters in comparison to o200k_base: going from
FIRST_KK to SECOND_KK, cl100k goes up (36 to 40) while o200k actually goes down (20 to
17).

3. COMPLAINT_JSON
------------------------------------------------------------------
                         EN           RU           KK
o200k_base               83          107          123
  ÷ EN                1.00x        1.29x        1.48x
cl100k_base              82          155          216
  ÷ EN                1.00x        1.89x        2.63x

On o200k_base the numbers are drastically changed for en and ru (+24 and +27 tokens),
however kk barely changes (118 to 123), almost the same as the non-json
version. On cl100k_base the pattern is different: en and ru still increase, but kk
actually goes down (265 to 216) instead of staying flat, so for
this tokenizer kk is not "unchanged", it moves the most of all three languages, just in
the opposite direction.