package br.com.barberagenda.service;

import java.time.Duration;
import java.time.LocalDateTime;

import org.springframework.stereotype.Component;

import br.com.barberagenda.exception.CancelamentoForaDoPrazoException;
import br.com.barberagenda.model.Agendamento;

/**
 * RF-09 — o cliente só pode cancelar com antecedência mínima em relação ao início do atendimento.
 * Regra criada pelo ciclo de TDD (Marco 9) e isolada nesta classe na etapa de refatoração.
 */
@Component
public class PoliticaCancelamento {

    public static final Duration ANTECEDENCIA_MINIMA = Duration.ofHours(2);

    static final String MENSAGEM = "O cancelamento só pode ser feito com no mínimo "
            + ANTECEDENCIA_MINIMA.toHours() + " horas de antecedência.";

    /** Recusa o cancelamento quando faltar menos que a antecedência mínima para o início (exatamente 2h é permitido). */
    public void validarPrazo(Agendamento agendamento, LocalDateTime agora) {
        if (agendamento.getDataHoraInicio().isBefore(agora.plus(ANTECEDENCIA_MINIMA))) {
            throw new CancelamentoForaDoPrazoException(MENSAGEM);
        }
    }
}
