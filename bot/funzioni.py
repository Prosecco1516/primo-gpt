def determina_sede(messaggio):
    messaggio = messaggio.lower()
    if any(x in messaggio for x in ["pneumatic", "gomme", "stagionali", "convergenza"]):
        return "Pneumatici"
    elif any(x in messaggio for x in ["meccanica", "revisione", "tagliando", "freni", "motore"]):
        return "Meccanica e Revisioni"
    elif any(x in messaggio for x in ["lucidatura", "coating", "ppf", "lavaggio", "interni"]):
        return "Detailing"
    else:
        return "Non specificato"
