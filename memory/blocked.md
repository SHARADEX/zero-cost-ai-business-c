# Blocked Actions Log — v4.1 (Autonomous Edition)

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 37.654104165s.",
    "status": "RESOURCE_E
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/g
CIRCUIT_OPEN gemini
FAIL cerebras/gemma-4-31b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
FAIL cerebras/gpt-oss-120b attempt 1: HTTP 402: {"message":"Pay

[2026-08-30 16:04:00 UTC] LLM call failed at step 3.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

SKIP gemini - unhealthy (circuit breaker)
FAIL cerebras/gemma-4-31b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
FAIL cerebras/gpt-oss-120b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
SKIP openrouter - budget exhausted

[2026-08-30 16:33:48 UTC] LLM call failed at step 1.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

CIRCUIT_OPEN groq
SKIP gemini - unhealthy (circuit breaker)
FAIL cerebras/gpt-oss-120b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
FAIL cerebras/gemma-4-31b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
SKIP openrouter - budget exhausted

[2026-08-30 17:03:45 UTC] LLM call failed at step 1.
All LLM providers failed. Attempts:
SKIP groq - unhealthy (circuit breaker)
SKIP gemini - unhealthy (circuit breaker)
FAIL cerebras/gemma-4-31b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
FAIL cerebras/gpt-oss-120b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
SKIP openrouter - budget exhausted

[2026-08-30 19:55:56 UTC] Agent output failed validation twice. Last error: No JSON object found. Output a single JSON object with no prose before or after.

[2026-08-30 19:55:56 UTC] LLM call failed at step 2.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 4.89388551s.",
    "status": "RESOURCE_EXH
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/g
FAIL gemini/gemma-4-26b-a4b-it attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor 

[2026-08-30 22:22:02 UTC] Agent output failed validation twice. Last error: No JSON object found. Output a single JSON object with no prose before or after.

[2026-08-30 22:22:02 UTC] LLM call failed at step 2.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 11.553620834s.",
    "status": "RESOURCE_E
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/g
FAIL gemini/gemma-4-26b-a4b-it attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor 

[2026-08-31 09:01:50 UTC] Agent output failed validation twice. Last error: No JSON object found. Output a single JSON object with no prose before or after.

[2026-08-31 09:01:50 UTC] LLM call failed at step 2.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 28.436561155s.",
    "status": "RESOURCE_E
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_c
FAIL gemini/gemma-4-26b-a4b-it attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor 

[2026-08-31 14:45:09 UTC] LLM call failed at step 2.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 912.11877ms.",
    "status": "RESOURCE_EXH
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_c
FAIL gemini/gemma-4-26b-a4b-it attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor 

[2026-08-31 20:35:24 UTC] Agent output failed validation twice. Last error: No JSON object found. Output a single JSON object with no prose before or after.

[2026-08-31 20:35:24 UTC] LLM call failed at step 2.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 59.504143039s.",
    "status": "RESOURCE_E
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_c
FAIL gemini/gemma-4-26b-a4b-it attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor 

[2026-09-01 10:17:46 UTC] LLM call failed at step 3.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

SKIP gemini - unhealthy (circuit breaker)
FAIL cerebras/gpt-oss-120b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
FAIL cerebras/gemma-4-31b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
SKIP openrouter - budget exhausted
