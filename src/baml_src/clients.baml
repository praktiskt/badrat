client<llm> Groq {
  provider "openai-generic"
  options {
    base_url "https://api.groq.com/openai/v1"
    model "llama-3.3-70b-versatile"
    api_key env.GROQ_API_KEY
    temperature 0
  }
}
