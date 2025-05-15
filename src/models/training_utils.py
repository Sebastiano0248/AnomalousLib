import torch

def _get_loss_name(criterion):
    # Puedes añadir más casos según tus criterios
    name_map = {
        "CrossEntropyLoss": "CE Loss",
        "MSELoss": "MSE Loss",
        "BCELoss": "BCE Loss",
        "BCEWithLogitsLoss": "BCEWithLogits Loss"
    }
    crit_name = type(criterion).__name__
    return name_map.get(crit_name, "Loss")

def train_model(model, train_loader, criterion, optimizer, patience=5, num_epochs=50, val_loader=None, scheduler=None, print_epoch=True):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    best_val_acc = 0.0
    counter = 0
    loss_name = _get_loss_name(criterion)

    for epoch in range(num_epochs):
        # Entrenamiento
        model.train()
        train_loss = 0.0
        for inputs, labels in train_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            
            train_loss += loss.item() * inputs.size(0)
        
        if scheduler is not None:
            scheduler.step()
        
        if print_epoch:
            print(f"Epoch {epoch+1}/{num_epochs}")
            print(f"Train {loss_name}: {train_loss/len(train_loader.dataset):.4f}", end="")

        # Validación solo si val_loader está definido
        if val_loader is not None:
            model.eval()
            val_loss = 0.0
            correct = 0
            total = 0
            with torch.no_grad():
                for inputs, labels in val_loader:
                    inputs = inputs.to(device)
                    labels = labels.to(device)
                    
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)
                    
                    val_loss += loss.item() * inputs.size(0)
                    _, predicted = torch.max(outputs.data, 1)
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()
            
            val_acc = 100 * correct / total
            if print_epoch:
                print(f" | Val {loss_name}: {val_loss/len(val_loader.dataset):.4f}")
                print(f"Val Accuracy: {val_acc:.2f}%")
            
            # Early stopping y guardar mejor modelo
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                torch.save(model.state_dict(), "best_model.pth")
                counter = 0
            else:
                counter += 1
                if counter >= patience:
                    print("Early stopping!")
                    break