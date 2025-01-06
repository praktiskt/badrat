class KeyValue {
  parameter_path string
  value string
}

class ResultSlim {
  possibly_dangerous bool
}

class ResultComplete {
  possibly_dangerous bool
  dangerous_parameters KeyValue[]
}

function ClassifyDangerousSlim(payload: string) -> ResultSlim {
  client "Groq"
  prompt #"
    Determine whether the following request is malicious:
    <REQUEST>{{ payload }}</REQUEST>

    Only respond with JSON.

    {{ ctx.output_format }}
  "#
}

function ClassifyDangerousComplete(payload: string) -> ResultComplete {
  client "Groq"
  prompt #"
    Determine whether the following request is malicious:
    <REQUEST>{{ payload }}</REQUEST>

    Only respond with JSON.

    {{ ctx.output_format }}
  "#
}
