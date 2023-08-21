from condaforge/mambaforge

RUN git clone https://github.com/szymonrucinski/AiRoll
RUN cd AiRoll
RUN git clone https://huggingface.co/szymonrucinski/what-a-shot
RUN mv what-a-shot model
RUN mamba env create -f env.yml
RUN conda activate AiRoll
RUN gradio start_api.py
EXPOSE 7860
