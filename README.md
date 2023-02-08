# Azure Cognitive Services for Language
A repo to consolidate a number of helpful scripts to experiment with Azure Cognitive Services for language.
- For text analytics, focusing on only five capabilities: sentiment, PII, key phrases, entity recognition and
summarization. For each capability, have a default sample, but can also add free text, and/or use the default
file with a number of statements.
- For the ingestion client, refer the following guide: https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/ingestion/ingestion-client/Setup/guide.md)

- Custom text classification example: https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/textanalytics/azure-ai-textanalytics/samples/sample_multi_label_classify.py

## Resources

```python
t = textAnalytics()

print(f"Entity recognition:\n")
t.entity_recognition(use_file=True)
t.entity_recognition(free_text="There are so many things to see in Portland! For example, I ate sushi for the first time!")
t.entity_recognition()

print(f"Sentiment:\n")
t.sentiment(use_file=True)
t.sentiment(free_text="I wish that this call would get over faster!")
t.sentiment()

print(f"Key Phrase extraction:\n")
t.key_phrase_extraction(use_file=True)
t.key_phrase_extraction(free_text="In this place there are so many different species of birds!")
t.key_phrase_extraction()

print(f"PII data:\n")
t.pii_data(use_file=True)
t.pii_data(free_text="Yes, my VISA credit card is 2222-4422-2422-1987 with a CVV of 763 and my social security number is 234-12-1111.")
t.pii_data()

print(f"Document summarization:\n")
t.document_summarization()

```
