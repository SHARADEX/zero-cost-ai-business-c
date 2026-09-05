# Blocked Actions Log — v4.1 (Autonomous Edition)

FAIL gemini/gemini-

[2026-09-03 22:41:41 UTC] Agent output failed validation twice. Last error: No JSON object found. Output a single JSON object with no prose before or after.

[2026-09-03 22:41:41 UTC] LLM call failed at step 3.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 32.524992171s.",
    "status": "RESOURCE_E
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_c
CIRCUIT_OPEN gemini
FAIL cerebras/gemma-4-31b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
FAIL cerebras/gpt-oss-120b attempt 1: HTTP 402: {"message":"Pay

[2026-09-04 05:22:08 UTC] LLM call failed at step 5.
All LLM providers failed. Attempts:
SKIP groq - unhealthy (circuit breaker)
SKIP gemini - unhealthy (circuit breaker)
FAIL cerebras/gpt-oss-120b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
CIRCUIT_OPEN cerebras
SKIP openrouter - budget exhausted

[2026-09-04 09:48:50 UTC] LLM call failed at step 2.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 31.54590128s.",
    "status": "RESOURCE_EX
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/g
FAIL gemini/gemma-4-26b-a4b-it attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor 

[2026-09-04 13:56:06 UTC] LLM call failed at step 2.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 30.417329525s.",
    "status": "RESOURCE_E
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_c
FAIL gemini/gemma-4-26b-a4b-it attempt 1: HTTP 503: {
  "error": {
    "code": 503,
    "message": "This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.",
    "status": "UNAVAILABLE"
  }
}

FAIL gemini/gemma-4-26b-a4b-it at

[2026-09-04 17:21:24 UTC] Agent output failed validation twice. Last error: No JSON object found. Output a single JSON object with no prose before or after.

[2026-09-04 17:21:24 UTC] LLM call failed at step 2.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 59.88589906s.",
    "status": "RESOURCE_EX
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_c
FAIL gemini/gemma-4-26b-a4b-it attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor 

[2026-09-04 19:45:43 UTC] LLM retry failed at step 2.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 34.353230136s.",
    "status": "RESOURCE_E
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/g
FAIL gemini/gemma-4-26b-a4b-it attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor 

[2026-09-04 19:45:43 UTC] LLM call failed at step 3.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

SKIP gemini - unhealthy (circuit breaker)
FAIL cerebras/llama-3.1-8b-instant attempt 1: HTTP 401: {"message":"Wrong API Key","type":"invalid_request_error","param":"api_key","code":"wrong_api_key"}
FAIL cerebras/llama3.1-70b attempt 1: HTTP 401: {"message":"Wrong API Key","type":"invalid_request_error","param":"api_key","code":"wrong_api_key"}
SKIP openrouter - budget exhausted

[2026-09-04 22:01:30 UTC] LLM retry failed at step 2.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 42.664307639s.",
    "status": "RESOURCE_E
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/g
FAIL gemini/gemma-4-26b-a4b-it attempt 1: gemini returned empty text in first part
CIRCUIT_OPEN gemini
FAIL cerebras/llama-3.1-8b-instant attempt 1: HTTP 401: {"message":"Wrong API Key","type":"invalid_request_error","param":"api_key","code":"wrong_api_key"}
FAIL cerebras/llama3.1-70

[2026-09-04 22:01:30 UTC] LLM call failed at step 3.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

SKIP gemini - unhealthy (circuit breaker)
FAIL cerebras/llama-3.1-8b-instant attempt 1: HTTP 401: {"message":"Wrong API Key","type":"invalid_request_error","param":"api_key","code":"wrong_api_key"}
FAIL cerebras/llama3.1-70b attempt 1: HTTP 401: {"message":"Wrong API Key","type":"invalid_request_error","param":"api_key","code":"wrong_api_key"}
SKIP openrouter - budget exhausted

[2026-09-05 00:14:08 UTC] revenue_verify error: Failed to fetch balance for ethereum
