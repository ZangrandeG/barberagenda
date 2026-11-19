package br.com.barberagenda.integration;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.time.Clock;
import java.time.LocalDateTime;
import java.time.ZoneId;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Primary;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import br.com.barberagenda.repository.BarbeiroRepository;
import br.com.barberagenda.repository.ServicoRepository;
import br.com.barberagenda.seed.CargaDadosFicticios;

/**
 * Integração (controller → service → banco) da regra criada por TDD (RF-09): cancelar com menos de 2 horas de
 * antecedência responde HTTP 422. O "agora" é fixado em quarta-feira, 18/11/2026, 09:00.
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@DisplayName("Integração — antecedência mínima para cancelamento (RF-09)")
class CancelamentoAntecedenciaIntegracaoTest {

    private static final ZoneId FUSO = ZoneId.of("America/Sao_Paulo");
    private static final LocalDateTime AGORA = LocalDateTime.of(2026, 11, 18, 9, 0);

    @TestConfiguration
    static class RelogioFixo {
        @Bean
        @Primary
        Clock relogioFixo() {
            return Clock.fixed(AGORA.atZone(FUSO).toInstant(), FUSO);
        }
    }

    @Autowired
    private MockMvc mvc;
    @Autowired
    private ObjectMapper json;
    @Autowired
    private CargaDadosFicticios carga;
    @Autowired
    private BarbeiroRepository barbeiroRepository;
    @Autowired
    private ServicoRepository servicoRepository;

    @BeforeEach
    void restaurarDados() {
        carga.recarregar();
    }

    private String agendarHoje(String horario) throws Exception {
        long carlos = barbeiroRepository.findByAtivoTrueOrderByNomeAsc().stream()
                .filter(b -> b.getNome().equals("Carlos Navalha")).findFirst().orElseThrow().getId();
        long corte = servicoRepository.findByAtivoTrueOrderByNomeAsc().stream()
                .filter(s -> s.getNome().equals("Corte de cabelo")).findFirst().orElseThrow().getId();
        String corpo = """
                {"emailCliente":"ana.rocha@exemplo.com","barbeiroId":%d,"servicoId":%d,"dataHoraInicio":"2026-11-18T%s:00"}
                """.formatted(carlos, corte, horario);
        String resposta = mvc.perform(post("/api/agendamentos").contentType(MediaType.APPLICATION_JSON).content(corpo))
                .andExpect(status().isCreated()).andReturn().getResponse().getContentAsString();
        JsonNode agendamento = json.readTree(resposta);
        return agendamento.get("codigoAcesso").asText();
    }

    @Test
    @DisplayName("RF-09 (TDD) / CT-036 — cancelar 1h30 antes do horário responde 422 com mensagem explicativa")
    void deveResponder422AoCancelarComMenosDeDuasHoras() throws Exception {
        String codigo = agendarHoje("10:30");

        mvc.perform(patch("/api/agendamentos/" + codigo + "/cancelar").contentType(MediaType.APPLICATION_JSON)
                        .content("{\"email\":\"ana.rocha@exemplo.com\"}"))
                .andExpect(status().isUnprocessableEntity())
                .andExpect(jsonPath("$.status").value(422))
                .andExpect(jsonPath("$.mensagem").value("O cancelamento só pode ser feito com no mínimo 2 horas de antecedência."));
    }

    @Test
    @DisplayName("RF-09 (TDD) / CT-036 — cancelar exatamente 2 horas antes é permitido")
    void devePermitirCancelarComExatamenteDuasHoras() throws Exception {
        String codigo = agendarHoje("11:00");

        mvc.perform(patch("/api/agendamentos/" + codigo + "/cancelar").contentType(MediaType.APPLICATION_JSON)
                        .content("{\"email\":\"ana.rocha@exemplo.com\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("CANCELADO"));
    }
}
