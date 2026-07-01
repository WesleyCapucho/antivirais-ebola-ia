import tensorflow as tf

@tf.keras.utils.register_keras_serializable(name="ConfidenceWeightedMSE")
def confidence_weighted_mse(y_true, y_pred, confidence_weights=None):
    """
    Função de Perda Customizada (Confidence-Weighted Mean Squared Error).
    Pune o erro de predição multiplicando-o pelo peso de confiança da fonte metodológica.
    Tier 1 (Enzimático) -> Peso 1.0 (Penalidade Total se errar)
    Tier 2 (Fenotípico) -> Peso 0.7
    Tier 3 (Classe)     -> Peso 0.5 (Penalidade Mitigada)
    """
    error_sq = tf.square(y_true - y_pred)
    
    if confidence_weights is not None:
        # Garante que os pesos tenham a mesma dimensão (batch_size, 1)
        weights = tf.cast(confidence_weights, dtype=tf.float32)
        weighted_error = error_sq * weights
        return tf.reduce_mean(weighted_error)
    else:
        # Fallback para MSE padrão se não passar os pesos
        return tf.reduce_mean(error_sq)

class CW_MSE_Layer(tf.keras.losses.Loss):
    """
    Classe para instanciar a Loss com pesos (para ser usada no Keras .compile()).
    O y_true deve ser empacotado como [valor_real, peso_confianca].
    """
    def __init__(self, name="confidence_weighted_mse", **kwargs):
        super().__init__(name=name, **kwargs)

    def call(self, y_true, y_pred):
        # y_true[:, 0] = Valores Reais de EC50
        # y_true[:, 1] = Confidence Scores (1.0, 0.7, 0.5)
        true_values = tf.expand_dims(y_true[:, 0], axis=-1)
        confidence = tf.expand_dims(y_true[:, 1], axis=-1)
        return confidence_weighted_mse(true_values, y_pred, confidence)
