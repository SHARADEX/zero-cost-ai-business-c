# Blocked Actions Log — v4.1 (Autonomous Edition)

FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 38.933643792s.",
    "status": "RESOURCE_E
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/g
FAIL gemini/gemma-4-26b-a4b-it attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor 

[2026-08-17 23:48:47 UTC] LLM call failed at step 1.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

SKIP gemini - unhealthy (circuit breaker)
FAIL cerebras/gemma-4-31b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
FAIL cerebras/gpt-oss-120b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
SKIP openrouter - budget exhausted

[2026-08-18 03:10:54 UTC] Agent output failed validation twice. Last error: No JSON object found. Output a single JSON object with no prose before or after.

[2026-08-18 05:04:47 UTC] LLM call failed at step 5.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

CIRCUIT_OPEN groq
SKIP gemini - unhealthy (circuit breaker)
FAIL cerebras/gemma-4-31b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
FAIL cerebras/gpt-oss-120b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
SKIP openrouter - budget exhausted

[2026-08-18 07:26:09 UTC] LLM call failed at step 3.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 36.034902422s.",
    "status": "RESOURCE_E
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_c
CIRCUIT_OPEN gemini
FAIL cerebras/gemma-4-31b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
FAIL cerebras/gpt-oss-120b attempt 1: HTTP 402: {"message":"Pay

[2026-08-18 09:06:21 UTC] LLM call failed at step 2.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 4.208443572s.",
    "status": "RESOURCE_EX
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/g
FAIL gemini/gemma-4-26b-a4b-it attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor 

[2026-08-18 10:55:27 UTC] LLM call failed at step 3.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 6.892040874s.",
    "status": "RESOURCE_EX
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_c
CIRCUIT_OPEN gemini
FAIL cerebras/gpt-oss-120b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
FAIL cerebras/gemma-4-31b attempt 1: HTTP 402: {"message":"Pay

[2026-08-18 11:55:48 UTC] LLM call failed at step 1.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash attempt 1: HTTP 404: {
  "error": {
    "code": 404,
    "message": "This model models/gemini-2.5-flash is no longer available to new users. Please update your code to use models/gemini-3.6-flash for the latest features and improvements.",
    "status": "NOT_FOUND"
  }
}

FAIL gemini/gemini-2.5-pro attempt 1: HTTP 404: {
  "error": {
    "code": 404,
    "message": "This model models/gemini-2.5-pro is no longer available to new users. Please update your code to use models/gemini-3.1-pro-preview for the latest features and improvements.",
    "status": "NOT_FOUND"
  }
}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 9.969139255s.",
    "status": "RESOURCE_EX
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://a

[2026-08-18 14:05:37 UTC] LLM call failed at step 3.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 1.221554362s.",
    "status": "RESOURCE_EX
CIRCUIT_OPEN gemini
FAIL cerebras/gpt-oss-120b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
FAIL cerebras/gemma-4-31b attempt 1: HTTP 402: {"message":"Payment required to access this resource. Visit your billing tab.","type":"payment_required_error","param":"quota","code":"payment_required"}
SKIP openrouter - budget exhausted

[2026-08-18 15:57:30 UTC] Agent output failed validation twice. Last error: No JSON object found. Output a single JSON object with no prose before or after.

[2026-08-18 15:57:30 UTC] LLM call failed at step 2.
All LLM providers failed. Attempts:
FAIL groq/meta-llama/llama-prompt-guard-2-86m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL groq/meta-llama/llama-prompt-guard-2-22m attempt 1: HTTP 400: {"error":{"message":"`max_tokens` must be less than or equal to `512`, the maximum value for `max_tokens` is less than the `context_window` for this model","type":"invalid_request_error","param":"max_tokens"}}

FAIL gemini/gemini-2.5-flash-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 10000, model: gemini-2.5-flash-tts\nPlease retry in 4.052602192s.",
    "status": "RESOURCE_EX
FAIL gemini/gemini-2.5-pro-preview-tts attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.5-pro-tts\n* Quota exceeded for metric: generativelanguage.googleapis.com/g
FAIL gemini/gemma-4-26b-a4b-it attempt 1: HTTP 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor 
