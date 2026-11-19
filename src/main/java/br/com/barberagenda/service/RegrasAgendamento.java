package br.com.barberagenda.service;

import java.time.Clock;
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Component;

import br.com.barberagenda.exception.RegraNegocioException;

/**
 * Regras de data e hora dos agendamentos (RN-04, RN-05 e RN-06).
 * Usa o {@link Clock} injetado para obter o momento atual.
 */
@Component
public class RegrasAgendamento {

    public static final LocalTime ABERTURA = LocalTime.of(9, 0);
    public static final LocalTime FECHAMENTO = LocalTime.of(19, 0);
    public static final int INTERVALO_MINUTOS = 30;
    public static final int ANTECEDENCIA_MAXIMA_DIAS = 30;

    private static final String CAMPO_DATA_HORA = "dataHoraInicio";

    private final Clock relogio;

    public RegrasAgendamento(Clock relogio) {
        this.relogio = relogio;
    }

    public LocalDateTime agora() {
        return LocalDateTime.now(relogio);
    }

    /** Valida RN-06, RN-04 e RN-05, nesta ordem, para um agendamento que começa em {@code inicio}. */
    public void validarHorario(LocalDateTime inicio, int duracaoMinutos) {
        validarAntecedencia(inicio);
        validarFuncionamento(inicio, duracaoMinutos);
        validarIntervalo(inicio);
    }

    /** RN-06: não pode ser no passado e a data pode estar no máximo 30 dias à frente de hoje. */
    public void validarAntecedencia(LocalDateTime inicio) {
        LocalDateTime agora = agora();
        if (!inicio.isAfter(agora)) {
            throw new RegraNegocioException(CAMPO_DATA_HORA,
                    "Não é permitido agendar em data ou horário que já passou.");
        }
        if (inicio.toLocalDate().isAfter(agora.toLocalDate().plusDays(ANTECEDENCIA_MAXIMA_DIAS))) {
            throw new RegraNegocioException(CAMPO_DATA_HORA,
                    "A antecedência máxima para agendamento é de " + ANTECEDENCIA_MAXIMA_DIAS + " dias.");
        }
    }

    /** RN-04: segunda a sábado, das 09:00 às 19:00; o serviço precisa terminar até 19:00. */
    public void validarFuncionamento(LocalDateTime inicio, int duracaoMinutos) {
        if (DayOfWeek.SUNDAY.equals(inicio.getDayOfWeek())) {
            throw new RegraNegocioException(CAMPO_DATA_HORA, "A barbearia não abre aos domingos.");
        }
        LocalDateTime abertura = inicio.toLocalDate().atTime(ABERTURA);
        LocalDateTime fechamento = inicio.toLocalDate().atTime(FECHAMENTO);
        LocalDateTime fim = inicio.plusMinutes(duracaoMinutos);
        if (inicio.isBefore(abertura) || fim.isAfter(fechamento)) {
            throw new RegraNegocioException(CAMPO_DATA_HORA,
                    "O atendimento deve ocorrer entre 09:00 e 19:00 e o serviço precisa terminar até 19:00.");
        }
    }

    /** RN-05: o início deve cair em intervalos de 30 minutos (09:00, 09:30, ...). */
    public void validarIntervalo(LocalDateTime inicio) {
        if (inicio.getMinute() % INTERVALO_MINUTOS != 0 || inicio.getSecond() != 0 || inicio.getNano() != 0) {
            throw new RegraNegocioException(CAMPO_DATA_HORA,
                    "Os agendamentos devem começar em intervalos de 30 minutos (ex.: 09:00, 09:30).");
        }
    }

    /** Indica se a data aceita agendamentos: não é domingo, não é passada e está dentro de 30 dias. */
    public boolean dataAceitaAgendamentos(LocalDate data) {
        LocalDate hoje = agora().toLocalDate();
        return !DayOfWeek.SUNDAY.equals(data.getDayOfWeek())
                && !data.isBefore(hoje)
                && !data.isAfter(hoje.plusDays(ANTECEDENCIA_MAXIMA_DIAS));
    }

    /**
     * Gera os horários de início possíveis no dia para um serviço com a duração informada,
     * respeitando o funcionamento, o intervalo de 30 minutos e descartando horários já passados.
     * Não considera a ocupação do barbeiro.
     */
    public List<LocalDateTime> gerarHorariosDoDia(LocalDate data, int duracaoMinutos) {
        List<LocalDateTime> horarios = new ArrayList<>();
        if (!dataAceitaAgendamentos(data)) {
            return horarios;
        }
        LocalDateTime agora = agora();
        LocalDateTime fechamento = data.atTime(FECHAMENTO);
        for (LocalDateTime inicio = data.atTime(ABERTURA);
             !inicio.plusMinutes(duracaoMinutos).isAfter(fechamento);
             inicio = inicio.plusMinutes(INTERVALO_MINUTOS)) {
            if (inicio.isAfter(agora)) {
                horarios.add(inicio);
            }
        }
        return horarios;
    }
}
