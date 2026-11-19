package br.com.barberagenda.unit;

import static br.com.barberagenda.unit.DadosTeste.AGORA;
import static br.com.barberagenda.unit.DadosTeste.RELOGIO;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Optional;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import br.com.barberagenda.dto.ClienteRequest;
import br.com.barberagenda.exception.ConflitoException;
import br.com.barberagenda.model.Barbeiro;
import br.com.barberagenda.model.Cliente;
import br.com.barberagenda.repository.AgendamentoRepository;
import br.com.barberagenda.repository.BarbeiroRepository;
import br.com.barberagenda.repository.ClienteRepository;
import br.com.barberagenda.service.BarbeiroService;
import br.com.barberagenda.service.ClienteService;

@ExtendWith(MockitoExtension.class)
@DisplayName("ClienteService e BarbeiroService — unicidade de e-mail e exclusão de barbeiro")
class CadastroServiceTest {

    @Mock
    private ClienteRepository clienteRepository;
    @Mock
    private BarbeiroRepository barbeiroRepository;
    @Mock
    private AgendamentoRepository agendamentoRepository;

    @Test
    @DisplayName("CT-006 / RF-01 — recusa cadastro com e-mail já cadastrado, mesmo em maiúsculas")
    void deveRejeitarCadastroComEmailJaCadastrado() {
        ClienteService service = new ClienteService(clienteRepository, RELOGIO);
        when(clienteRepository.existsByEmailIgnoreCase("ana.rocha@exemplo.com")).thenReturn(true);

        assertThatThrownBy(() -> service.cadastrar(new ClienteRequest("Ana Repetida", "14988776655", "ANA.ROCHA@EXEMPLO.COM")))
                .isInstanceOf(ConflitoException.class)
                .hasMessage("Já existe um cliente cadastrado com este e-mail.");
        verify(clienteRepository, never()).save(any());
    }

    @Test
    @DisplayName("CT-001 / RF-01 — cadastra cliente com dados válidos e data de cadastro do relógio")
    void deveCadastrarClienteComDadosValidos() {
        ClienteService service = new ClienteService(clienteRepository, RELOGIO);
        when(clienteRepository.existsByEmailIgnoreCase("marina@exemplo.com")).thenReturn(false);
        when(clienteRepository.save(any(Cliente.class))).thenAnswer(invocacao -> invocacao.getArgument(0));

        Cliente cliente = service.cadastrar(new ClienteRequest("  Marina Lopes  ", "14988776655", "Marina@Exemplo.com"));

        assertThat(cliente.getNome()).isEqualTo("Marina Lopes");
        assertThat(cliente.getEmail()).isEqualTo("marina@exemplo.com");
        assertThat(cliente.getDataCadastro()).isEqualTo(AGORA);
    }

    @Test
    @DisplayName("CT-033 / RF-07 — recusa excluir barbeiro que possui agendamentos")
    void deveRejeitarExclusaoDeBarbeiroComAgendamentos() {
        BarbeiroService service = new BarbeiroService(barbeiroRepository, agendamentoRepository);
        when(barbeiroRepository.findById(1L)).thenReturn(Optional.of(new Barbeiro("Carlos Navalha", true)));
        when(agendamentoRepository.existsByBarbeiroId(1L)).thenReturn(true);

        assertThatThrownBy(() -> service.excluir(1L))
                .isInstanceOf(ConflitoException.class)
                .hasMessage("O barbeiro possui agendamentos e não pode ser excluído. Desative-o em vez de excluir.");
        verify(barbeiroRepository, never()).delete(any());
    }

    @Test
    @DisplayName("CT-033 / RF-07 — exclui barbeiro sem agendamentos")
    void deveExcluirBarbeiroSemAgendamentos() {
        BarbeiroService service = new BarbeiroService(barbeiroRepository, agendamentoRepository);
        Barbeiro temporario = new Barbeiro("Barbeiro Temporário", true);
        when(barbeiroRepository.findById(9L)).thenReturn(Optional.of(temporario));
        when(agendamentoRepository.existsByBarbeiroId(9L)).thenReturn(false);

        service.excluir(9L);

        verify(barbeiroRepository).delete(temporario);
    }
}
