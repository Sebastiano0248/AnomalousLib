from anomalouslib.data.DatasetGenerator import DatasetGenerator

try:
    print("Testing DatasetGenerator...")

    dg = DatasetGenerator(num_particules=10)
    dg.changeParams(num_particules=None)
    dg.changeParams(num_particules=100)
    rw_dataset = dg.generate_RandomWalk(num_passos=100, random_params=True)
    bm_dataset = dg.generate_BrownianMotion(num_passos=100, random_params=True)
    fbm_dataset = dg.generate_FractionalBrownianMotion(num_passos=100, random_params=True)
    ctrw_dataset = dg.generate_ContinuousTimeRandomWalk(num_passos=100, random_params=True)
    lw_dataset = dg.generate_LevyWalks(num_passos=100, random_params=True)
    attm_dataset = dg.generate_AnnealedTransitTimeModel(num_passos=100, random_params=True)
    sbm_dataset = dg.generate_ScaledBrownianMotion(num_passos=100, random_params=True)

except Exception as e:
    print(f"An error occurred during the test: {e}")
else:
    print("DatasetGenerator test completed successfully.")



from anomalouslib.data.preprocessing import generate_tensors

try:
    print("Testing preprocessing functions...")
    dg = DatasetGenerator(num_particules=10)
    fbm_dataset = dg.generate_FractionalBrownianMotion(num_passos=100, random_params=True)
    generate_tensors(fbm_dataset, "Fractional Brownian Motion", "hurst")

except Exception as e:
    print(f"An error occurred during the test: {e}")
else:
    print("Preprocessing functions test completed successfully.")