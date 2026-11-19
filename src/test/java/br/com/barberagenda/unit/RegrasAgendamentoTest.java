package br.com.barberagenda.unit;

import static br.com.barberagenda.unit.DadosTeste.D_MAIS_30;
import static br.com.barberagenda.unit.DadosTeste.D_MAIS_31;
import static br.com.barberagenda.unit.DadosTeste.DF3;
import static br.com.barberagenda.unit.DadosTeste.DOMINGO;
import static br.com.barberagenda.unit.DadosTeste.HOJE;
import static br.com.barberagenda.unit.DadosTeste.ONTEM;
import static br.com.barberagenda.unit.DadosTeste.RELOGIO;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatCode;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Stream;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import br.com.barberagenda.exception.RegraNegocioException;
import br.com.barberagenda.service.RegrasAgendamento;

@DisplayName("RegrasAgendamento — funcionamento, intervalo e antecedência (RN-04, RN-05, RN-06)")
class RegrasAgendamentoTest {

    private static final String MSG_FUNCIONAMENTO =
            "O atendimento deve ocorrer entre 09:00 e 19:00 e o serviço precisa terminar até 19:00.";
    private static final String MSG_INTERVALO =
            "Os agendamentos devem começar em intervalos de 30 minutos (ex.: 09:00, 09:30).";
    private static final String MSG_PASSADO = "Não é permitido agendar em data ou horário que já passou.";

    private final RegrasAgendamento regras = new RegrasAgendamento(RELOGIO);

    @Test
    @DisplayName("CT-007 / RF-02 — serviço de 60 min tem 19 inícios possíveis, de 09:00 a 18:00, de 30 em 30 min")
    void deveGerarHorariosDe09hA18hParaServicoDe60Minutos() {
        List<LocalDateTime> horarios = regras.gerarHorariosDoDia(DF3, 60);

        assertThat(horarios).hasSize(20); // QUEBRA PROPOSITAL: demonstração de falha no pipeline (não é defeito do sistema)
        assertThat(horarios.get(0)).isEqualTo(DF3.atTime(9, 0));
        assertThat(horarios.get(horarios.size() - 1)).isEqualTo(DF3.atTime(18, 0));
        assertThat(horarios).extracting(LocalDateTime::getMinute).containsOnly(0, 30);
    }

    @Test
    @DisplayName("RF-02 — no dia de hoje não são oferecidos horários que já passaram (agora = 10:00)")
    void naoDeveOferecerHorariosJaPassadosNoDiaDeHoje() {
        List<LocalDateTime> horarios = regras.gerarHorariosDoDia(HOJE, 30);

        assertThat(horarios.get(0)).isEqualTo(HOJE.atTime(10, 30));
        assertThat(horarios).allMatch(inicio -> inicio.isAfter(DadosTeste.AGORA));
    }

    static Stream<Arguments> datasSemAtendimento() {
        return Stream.of(
                Arguments.of("domingo", DOMINGO),
                Arguments.of("D+31", D_MAIS_31),
                Arguments.of("ontem", ONTEM));
    }

    @ParameterizedTest(name = "{0}")
    @MethodSource("datasSemAtendimento")
    @DisplayName("CT-009 / RF-02 — data sem atendimento não tem horários disponíveis")
    void deveRetornarListaVaziaParaDataSemAtendimento(String descricao, LocalDate data) {
        assertThat(regras.gerarHorariosDoDia(data, 30)).isEmpty();
    }

    static Stream<Arguments> limitesValidosDoFuncionamento() {
        return Stream.of(
                Arguments.of("início 09:00, 30 min", DF3.atTime(9, 0), 30),
                Arguments.of("início 18:30, 30 min (termina 19:00)", DF3.atTime(18, 30), 30),
                Arguments.of("início 18:00, 60 min (termina 19:00)", DF3.atTime(18, 0), 60));
    }

    @ParameterizedTest(name = "{0}")
    @MethodSource("limitesValidosDoFuncionamento")
    @DisplayName("CT-011 / RF-03 — aceita agendamento nos limites do horário de funcionamento")
    void deveAceitarAgendamentoNosLimitesDoFuncionamento(String descricao, LocalDateTime inicio, int duracao) {
        assertThatCode(() -> regras.validarHorario(inicio, duracao)).doesNotThrowAnyException();
    }

    static Stream<Arguments> limitesInvalidosDoFuncionamento() {
        return Stream.of(
                Arguments.of("início 08:30", DF3.atTime(8, 30), 30),
                Arguments.of("início 18:30, 60 min (terminaria 19:30)", DF3.atTime(18, 30), 60));
    }

    @ParameterizedTest(name = "{0}")
    @MethodSource("limitesInvalidosDoFuncionamento")
    @DisplayName("CT-012 / RF-03 — recusa agendamento que começa antes de 09:00 ou termina depois de 19:00")
    void deveRejeitarAgendamentoForaDoHorarioDeFuncionamento(String descricao, LocalDateTime inicio, int duracao) {
        assertThatThrownBy(() -> regras.validarHorario(inicio, duracao))
                .isInstanceOf(RegraNegocioException.class)
                .hasMessage(MSG_FUNCIONAMENTO);
    }

    @ParameterizedTest(name = "início {0}")
    @MethodSource("iniciosForaDoIntervalo")
    @DisplayName("CT-013 / RF-03 — recusa início fora dos intervalos de 30 minutos")
    void deveRejeitarInicioForaDoIntervaloDe30Minutos(LocalDateTime inicio) {
        assertThatThrownBy(() -> regras.validarHorario(inicio, 30))
                .isInstanceOf(RegraNegocioException.class)
                .hasMessage(MSG_INTERVALO);
    }

    static Stream<LocalDateTime> iniciosForaDoIntervalo() {
        return Stream.of(DF3.atTime(10, 15), DF3.atTime(10, 1));
    }

    @Test
    @DisplayName("CT-014 / RF-03 — recusa agendamento no domingo")
    void deveRejeitarAgendamentoNoDomingo() {
        assertThatThrownBy(() -> regras.validarHorario(DOMINGO.atTime(10, 0), 30))
                .isInstanceOf(RegraNegocioException.class)
                .hasMessage("A barbearia não abre aos domingos.");
    }

    @Test
    @DisplayName("CT-015 / RF-03 — aceita agendamento com exatamente 30 dias de antecedência (D+30)")
    void deveAceitarAgendamentoComTrintaDiasDeAntecedencia() {
        assertThatCode(() -> regras.validarHorario(D_MAIS_30.atTime(10, 0), 30)).doesNotThrowAnyException();
    }

    @Test
    @DisplayName("CT-015 / RF-03 — recusa agendamento com 31 dias de antecedência (D+31)")
    void deveRejeitarAgendamentoComTrintaEUmDiasDeAntecedencia() {
        assertThatThrownBy(() -> regras.validarHorario(D_MAIS_31.atTime(10, 0), 30))
                .isInstanceOf(RegraNegocioException.class)
                .hasMessage("A antecedência máxima para agendamento é de 30 dias.");
    }

    static Stream<Arguments> iniciosNoPassado() {
        return Stream.of(
                Arguments.of("ontem às 10:00", ONTEM.atTime(10, 0)),
                Arguments.of("hoje às 09:00 (agora = 10:00)", HOJE.atTime(9, 0)),
                Arguments.of("hoje às 10:00 (exatamente agora)", HOJE.atTime(10, 0)));
    }

    @ParameterizedTest(name = "{0}")
    @MethodSource("iniciosNoPassado")
    @DisplayName("CT-016 / RF-03 — recusa agendamento em data ou horário que já passou")
    void deveRejeitarAgendamentoNoPassado(String descricao, LocalDateTime inicio) {
        assertThatThrownBy(() -> regras.validarHorario(inicio, 30))
                .isInstanceOf(RegraNegocioException.class)
                .hasMessage(MSG_PASSADO);
    }

    @Test
    @DisplayName("CT-016 / RF-03 — aceita o próximo horário do dia de hoje (10:30, com agora = 10:00)")
    void deveAceitarProximoHorarioDoDiaDeHoje() {
        assertThatCode(() -> regras.validarHorario(HOJE.atTime(10, 30), 30)).doesNotThrowAnyException();
    }
}
