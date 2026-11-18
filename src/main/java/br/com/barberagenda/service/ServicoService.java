package br.com.barberagenda.service;

import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import br.com.barberagenda.dto.ServicoRequest;
import br.com.barberagenda.exception.ConflitoException;
import br.com.barberagenda.exception.RecursoNaoEncontradoException;
import br.com.barberagenda.model.Servico;
import br.com.barberagenda.repository.AgendamentoRepository;
import br.com.barberagenda.repository.ServicoRepository;

@Service
public class ServicoService {

    private final ServicoRepository servicoRepository;
    private final AgendamentoRepository agendamentoRepository;

    public ServicoService(ServicoRepository servicoRepository, AgendamentoRepository agendamentoRepository) {
        this.servicoRepository = servicoRepository;
        this.agendamentoRepository = agendamentoRepository;
    }

    @Transactional(readOnly = true)
    public List<Servico> listarAtivos() {
        return servicoRepository.findByAtivoTrueOrderByNomeAsc();
    }

    @Transactional(readOnly = true)
    public List<Servico> listarTodos() {
        return servicoRepository.findAllByOrderByNomeAsc();
    }

    @Transactional(readOnly = true)
    public Servico buscar(Long id) {
        return servicoRepository.findById(id)
                .orElseThrow(() -> new RecursoNaoEncontradoException("Serviço não encontrado."));
    }

    /** RN-09 é validada no {@link ServicoRequest} (duração e preço). */
    @Transactional
    public Servico cadastrar(ServicoRequest dados) {
        Servico servico = new Servico(dados.nome(), dados.duracaoMinutos(), dados.preco(), dados.ativoOuPadrao());
        return servicoRepository.save(servico);
    }

    @Transactional
    public Servico atualizar(Long id, ServicoRequest dados) {
        Servico servico = buscar(id);
        servico.atualizar(dados.nome(), dados.duracaoMinutos(), dados.preco(), dados.ativoOuPadrao());
        return servico;
    }

    /** Exclui o serviço. Se ele já foi usado em agendamentos, a exclusão é recusada (use a desativação). */
    @Transactional
    public void excluir(Long id) {
        Servico servico = buscar(id);
        if (agendamentoRepository.existsByServicoId(id)) {
            throw new ConflitoException(
                    "O serviço possui agendamentos e não pode ser excluído. Desative-o em vez de excluir.");
        }
        servicoRepository.delete(servico);
    }
}
