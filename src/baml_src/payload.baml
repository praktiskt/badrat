class KeyValue {
  key string
  value string
}

class IsDangerous {
  possibly_dangerous bool
  dangerous_parameters KeyValue[] @description("Parameters that could indicate a dangerous request")
}

// Create a function to extract the resume from a string.
function ClassifyDangerous(payload: string) -> IsDangerous {
  client "Groq" // Set OPENAI_API_KEY to use this client.
  prompt #"
    Determine whether the following request is malicious, dangerous or attempting to do anything sketchy:
    <REQUEST>{{ payload }}</REQUEST>

    Never include anything but JSON in your response.

    {{ ctx.output_format }}
  "#
}
