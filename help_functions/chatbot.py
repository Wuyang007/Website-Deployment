from transformers import AutoTokenizer, T5ForConditionalGeneration, AutoModelForCausalLM

def generate_response(user_input):
    # Format the input as an instruction (Flan-T5 is instruction-tuned)
    model_name = "gpt2"  # You can replace this with other models like 'microsoft/DialoGPT-small'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    inputs = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    
    # Generate a response from the model
    response_ids = model.generate(inputs, max_length=200, pad_token_id=tokenizer.eos_token_id, 
                                  do_sample=True, temperature=0.7, top_p=0.9, num_return_sequences=1)
    
    # Decode the generated response back into text
    response = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    return response