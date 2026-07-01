import tensorflow as tf
from tensorflow.keras import layers

class MCDropout(layers.Dropout):
    """
    Implementação da camada de Monte Carlo Dropout.
    Diferente do Dropout convencional que desliga na inferência, esta camada
    se mantém ativa durante o predict() (training=True) para permitir a 
    amostragem estocástica e o cálculo da Incerteza Epistêmica.
    """
    def call(self, inputs, training=None):
        # Força o dropout a estar sempre ativo, inclusive em model.predict()
        return super().call(inputs, training=True)

def build_mc_dropout_model(input_dim):
    """
    Constrói a Rede Neural Profunda com camadas de MC Dropout embutidas.
    """
    inputs = tf.keras.Input(shape=(input_dim,))
    
    # Camada Oculta 1
    x = layers.Dense(512, activation='relu')(inputs)
    x = layers.BatchNormalization()(x)
    x = MCDropout(0.2)(x) # 20% de inibição constante
    
    # Camada Oculta 2
    x = layers.Dense(256, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = MCDropout(0.2)(x)
    
    # Camada Oculta 3
    x = layers.Dense(128, activation='relu')(x)
    x = MCDropout(0.1)(x)
    
    # Saída (Regressão: predição do EC50/pIC50)
    outputs = layers.Dense(1, activation='linear')(x)
    
    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="Ebola_Polymerase_MCDropout")
    return model
