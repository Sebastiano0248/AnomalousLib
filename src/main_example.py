# Ejemplo de uso
if __name__ == "__main__":
    # Crear y guardar dataset generado
    gen_data = GeneratedDataset("mi_dataset_generado")
    gen_data.generate_or_download(lambda: pd.DataFrame({'col': [1, 2, 3]}))
    gen_data.save("data/generated_dataset.pkl")
    
    # Cargar dataset
    loaded_data = Dataset.load("data/generated_dataset.pkl")
    
    # Analizar datos
    analyzer = DataAnalyzer(loaded_data)
    stats = analyzer.basic_statistics()
    
    # Procesar con modelo y guardar resultados
    class MiModelo(Model):
        def train(self, data, *args, **kwargs):
            # Implementar lógica de entrenamiento
            self.trained = True
        
        def predict(self, data, *args, **kwargs):
            # Implementar lógica de predicción
            return "resultado_ejemplo"
    
    model = MiModelo()
    model.train(loaded_data.data)
    predictions = model.predict(loaded_data.data)
    
    result_manager = ResultManager()
    result_manager.add_result("estadisticas", stats)
    result_manager.add_result("predicciones", predictions)
    result_manager.save_results("resultados/resultados_finales.pkl")