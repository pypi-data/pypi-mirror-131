# Model Parallelism

This package is a simple wrapper around [DeepSpeed](https://www.deepspeed.ai) to make it as easy as possible to implement model parallelism in your PyTorch models.

## Example Usage

```diff
  # Your training script
+ import model_parallelism

  # All your data preparation, logging, etc.

  model = create_model(...)

- model = model.to(device)
- optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
+ model = model_parallelism.initialize(
+     model, learning_rate=1e-4, optimizer="Adam", batch_size=batch_size
+ )

  for batch in dataloader:
      loss = model(batch)
-     loss.backward
+     model.backward(loss)
-     optimizer.step()
+     model.step()
```
