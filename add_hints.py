import json

data = json.load(open('questions.json'))

updates = {
    'parallelism': {
        'hints': [
            "Think about dividing a single layer's computation.",
            "It lets one part compute while another sends data.",
            "Consider what must be identical on each GPU.",
            "It's aimed at saving memory across workers.",
            "This operation shares gradient sums among GPUs.",
            "Empty slots form as the pipeline fills or drains.",
            "It splits matrices and sums partial results.",
            "You recompute activations to save space.",
            "Alternating forward and backward passes keeps stages busy.",
            "Large embeddings may be split across devices."
        ],
        'elabs': [
            "Tensor parallelism slices tensors so one layer spans multiple devices.",
            "Pipelining overlaps compute and communication across stages.",
            "Data parallelism replicates model weights on each device.",
            "ZeRO stage 3 shards parameters, gradients, and optimizer state.",
            "All-reduce sums gradients so every replica syncs.",
            "Bubble overhead comes from pipeline startup and drain time.",
            "Reduce-scatter distributes pieces of a matrix multiplication.",
            "Gradient checkpointing trades extra compute to reduce memory.",
            "The 1F1B schedule minimizes pipeline bubbles.",
            "Sharding embeddings is a form of model parallelism."
        ]
    },
    'inference': {
        'hints': [
            "It avoids recomputing attention for prior tokens.",
            "The bigger model checks the draft tokens.",
            "Aggregating multiple examples keeps the GPU busy.",
            "Think about aggressive quantization for deployment.",
            "Look at how attention sees only past positions.",
            "It manages key/value memory more flexibly.",
            "Nucleus sampling keeps only the most probable tokens.",
            "It explores multiple candidate sequences.",
            "It discards or combines redundant heads.",
            "They send partial results early."
        ],
        'elabs': [
            "Attention caching stores previously computed key/value pairs for reuse.",
            "The large model verifies proposed tokens from the small model.",
            "Batching improves overall throughput on the accelerator.",
            "Int8 quantization cuts memory with little accuracy drop.",
            "Causal masking forces generation one token at a time.",
            "Paged attention lets vLLM serve many concurrent prompts.",
            "Tokens outside the top-p mass are filtered out.",
            "Beam search spends more compute to get higher quality.",
            "Head pruning merges heads to reduce work.",
            "Streaming tokens lowers perceived latency for users."
        ]
    },
    'alignment': {
        'hints': [
            "Think about how humans judge outputs pairwise.",
            "It follows a set of written principles.",
            "Popular approach for ChatGPT-style models.",
            "Alignment features often slow things down.",
            "Models can game imperfect reward functions.",
            "It picks the safest of several responses.",
            "It includes adversarial examples to teach caution.",
            "Automated LM judges can scale better than humans.",
            "It's a recent alternative to PPO.",
            "A practice borrowed from security testing."
        ],
        'elabs': [
            "The reward model learns from human preference comparisons.",
            "Constitutional AI uses fixed self-consistency rules instead of human scores.",
            "Instruction tuning trains on prompt-completion pairs to follow directions.",
            "The alignment tax is extra compute spent on safety measures.",
            "Policies may exploit weaknesses in the reward model, known as reward hacking.",
            "Self-consistency decoding chooses a safe answer among many.",
            "Harmlessness training adds adversarially generated attacks during fine-tuning.",
            "Another language model often evaluates alignment automatically.",
            "Direct preference optimization updates the policy using the reward without rollouts.",
            "Red teaming searches for failure modes before deployment."
        ]
    },
    'agents': {
        'hints': [
            "One handles reasoning steps, the other triggers tools.",
            "It decides what action to take next.",
            "It shows the model how to call external APIs.",
            "Consider the cost of iterative reasoning.",
            "It's like the agent's memory log.",
            "Think of how the API encodes function parameters.",
            "It strings together multiple operations.",
            "Imagine operating software with persistent state.",
            "The model needs to know available tools.",
            "It runs code safely and reports errors." 
        ],
        'elabs': [
            "ReAct combines reasoning traces with actions such as tool calls.",
            "The policy or planner selects the next step in the loop.",
            "Toolformer inserts API calls into data to teach tool use.",
            "Agents use multiple model calls and tools, so they are pricier than single completions.",
            "A scratchpad records intermediate steps for context.",
            "Function calling returns structured JSON describing which tool to run.",
            "LangChain organizes sequences of tool invocations.",
            "Action-observation loops interact with external stateful systems.",
            "OpenAI's function calling requires API specifications describing tools.",
            "Sandboxed execution with error feedback reduces hallucinated code."]
    },
    'pretraining': {
        'hints': [
            "Think about predicting the next word.",
            "It ties compute to the amount of training data.",
            "They didn't see enough data for their size.",
            "Repeated examples can cause memorization.",
            "Bigger batches can converge to sharp minima.",
            "The model must reconstruct masked tokens.",
            "Start easy then move to harder examples.",
            "It's not byte-pair or wordpiece.",
            "Structured code can teach logical patterns.",
            "It indicates how noisy the gradients are." 
        ],
        'elabs': [
            "Cross-entropy on next token prediction is the standard loss for autoregressive LMs.",
            "Compute-optimal scaling balances parameters with dataset tokens.",
            "Chinchilla showed many models were undertrained on tokens.",
            "Deduplicating text reduces overfitting risk.",
            "Very large batches may hurt generalization.",
            "Masking leads to a denoising autoencoding objective.",
            "Curriculum learning varies data difficulty over time.",
            "SentencePiece often uses a unigram model for subwords.",
            "Mixing code and text can improve reasoning precision.",
            "Gradient noise scale measures how well larger batches work." ]
    },
    'retrieval': {
        'hints': [
            "Think of the retrieval step before generation.",
            "It's about fast similarity lookups.",
            "It merges lexical and semantic matches.",
            "It's part of the generator model.",
            "External documents can provide more knowledge.",
            "Classic bag-of-words ranking.",
            "Keeping the database up to date.",
            "Tune the graph parameters for accuracy.",
            "Allows comparing individual words.",
            "Think about positive and negative pairs." 
        ],
        'elabs': [
            "Query embeddings are matched against a document index.",
            "Faiss accelerates approximate nearest neighbor search.",
            "Hybrid search improves recall across document types.",
            "Fusion-in-decoder integrates retrieved passages into the context.",
            "Retrieval during pretraining provides grounding information.",
            "BM25 performs sparse lexical retrieval based on term frequency.",
            "Refreshing the index lets the model include new knowledge.",
            "HNSW parameters trade search accuracy for time.",
            "ColBERT's token-level embeddings enable fine-grained scoring.",
            "Dense retrieval commonly uses contrastive learning." ]
    },
    'gpus': {
        'hints': [
            "It's inside each streaming multiprocessor.",
            "Think of dense linear algebra.",
            "Data moves directly GPU-to-GPU.",
            "Measures how many warps are active.",
            "Launching many tiny kernels is inefficient.",
            "Gradients accumulate in higher precision.",
            "Pages data in and out automatically.",
            "They target matrix multiplications.",
            "Think concurrency.",
            "Fewer launches and less global memory access." 
        ],
        'elabs': [
            "Register files are the smallest and fastest GPU memory.",
            "Tensor cores speed up FP16 matrix multiplications.",
            "Peer-to-peer NVLink transfers avoid host CPU memory.",
            "SM occupancy best reflects compute utilization.",
            "Millions of very small kernels make launch overhead noticeable.",
            "Mixed precision keeps master weights in float32.",
            "Unified memory paging allows models larger than GPU memory.",
            "Tensor cores perform fused multiply-add matrix operations.",
            "GPU streams overlap compute and data transfers.",
            "Kernel fusion combines small kernels to cut memory traffic." ]
    },
    'scaling laws': {
        'hints': [
            "Think about the three main axes of scale.",
            "This paper revisited scaling after Kaplan.",
            "Think y = a x^k.",
            "More FLOPs typically yield better models.",
            "Too few examples for too big a model.",
            "It's about choosing model size vs. dataset size.",
            "Duplicated examples matter less.",
            "Look at how cross-entropy decreases.",
            "Consider arithmetic cost when models grow.",
            "Bigger models do worse on these tasks." 
        ],
        'elabs': [
            "Performance depends on model size, dataset size, and compute.",
            "The Chinchilla paper updated the optimal data/parameter ratio.",
            "A power law means growth follows a constant exponent.",
            "Scaling laws show performance rises smoothly with compute budget.",
            "Scaling beyond data availability leads to overfitting and diminishing returns.",
            "Compute-optimal scaling balances model parameters with training tokens.",
            "The effective data scaling law notes too much repetition hurts generalization.",
            "Training loss or perplexity is often plotted versus model size.",
            "Compute FLOPs dominate training cost at large scales.",
            "Inverse scaling describes performance degrading as models grow." ]
    },
    'linear algebra': {
        'hints': [
            "Inner dimensions cancel, outer remain.",
            "It's related to cosine similarity.",
            "It's widely used for PCA.",
            "This property simplifies diagonalization.",
            "Use the dot product of v with u.",
            "Its quadratic form is always positive.",
            "Like the Euclidean norm for matrices.",
            "They represent rotations or reflections.",
            "No need for full elimination.",
            "Think about the number of independent vectors." 
        ],
        'elabs': [
            "Multiplying m×k with k×n yields an m×n matrix.",
            "The dot product equals norms times the cosine of the angle between vectors.",
            "Singular value decomposition expresses a matrix as UΣV^T.",
            "Eigenvectors of a symmetric matrix are orthogonal.",
            "Projection scales u by (v·u)/(u·u).",
            "A positive definite matrix has all positive eigenvalues.",
            "The Frobenius norm is the square root of the sum of squared entries.",
            "Orthogonal matrices preserve vector norms.",
            "Forward or backward substitution solves triangular systems.",
            "Rank equals the dimension of both the row and column space." ]
    },
    'privacy': {
        'hints': [
            "It's about limiting knowledge of single records.",
            "Limits contribution of any one example.",
            "Uncommon phrases might reappear in outputs.",
            "It's about forgetting specific examples.",
            "Fake data can stand in for originals.",
            "Training happens locally.",
            "Secures data in transit.",
            "Attackers guess which examples the model saw.",
            "Encrypted arithmetic is slow.",
            "Student learns from an ensemble of teachers." 
        ],
        'elabs': [
            "Differential privacy bounds what an attacker can learn about any individual.",
            "Gradient clipping enforces bounded sensitivity in DPSGD.",
            "Memorizing rare sequences can leak personal data verbatim.",
            "Machine unlearning can remove data after training.",
            "Synthetic data avoids exposing real user records.",
            "Federated learning keeps raw data on each user's device.",
            "Encryption secures the communication channels carrying data.",
            "Membership inference tests if a record was in the training set.",
            "Homomorphic encryption is computationally expensive for neural nets.",
            "PATE relies on knowledge distillation with noise added." ]
    },
    'ethics': {
        'hints': [
            "Economists use this term for side effects.",
            "It's about problematic examples in the data.",
            "Think of documentation for models.",
            "People might think it's written by a human.",
            "Checking for disparities between populations.",
            "Better safe than sorry.",
            "A model is watching another model.",
            "Simulating adversarial users.",
            "Openness about weaknesses.",
            "Some groups may be missing in training data." 
        ],
        'elabs': [
            "Negative externalities are unintended harmful effects of deployment.",
            "Dataset curation reduces bias and offensive content.",
            "Model cards provide transparency in reporting.",
            "Undisclosed synthetic content may mislead users about authenticity.",
            "Fairness evaluations compare metrics across demographic groups.",
            "The precautionary principle suggests delaying deployment until risks are known.",
            "Using another language model for moderation is automated oversight.",
            "Red teaming finds potential misuse scenarios.",
            "Transparency encourages explaining model limitations clearly.",
            "Limiting data from certain groups can cause underrepresentation bias." ]
    },
    'interpretability': {
        'hints': [
            "Think of the matrices showing token influence.",
            "They assign a relevance value to each input.",
            "Neurons may represent more than one concept.",
            "Pieces of the network that compute a subtask.",
            "It swaps activations to see their effect.",
            "It names individual neuron behaviors.",
            "Looking at weights and activations directly.",
            "Sparse activations isolate distinct features.",
            "It removes parts to measure importance.",
            "Tracing which paths affect the output." 
        ],
        'elabs': [
            "Attention visualization focuses on the attention weights.",
            "Integrated Gradients yields per-token importance scores.",
            "Superposition means multiple features share the same direction.",
            "A circuit is a small group of weights implementing a function.",
            "Activation patching tests how specific activations change results.",
            "Automatic feature labeling tries to find neurons linked to concepts.",
            "Mechanistic interpretability studies weight and activation patterns.",
            "Sparse autoencoders promote disentangled representations.",
            "Causal scrubbing measures forgetting when features are ablated.",
            "Path patching identifies which intermediate paths drive behavior." ]
    },
    'mixture of experts': {
        'hints': [
            "It decides which experts to activate.",
            "Usually only a few experts get used.",
            "Some experts may get far more tokens than others.",
            "They 'switch' to a single route.",
            "The gate looks at the token representation.",
            "Skip the unused experts.",
            "Randomly disable some experts during training.",
            "It's a penalty for skewed routing.",
            "Low-importance tokens may be skipped.",
            "Structure is the same but weights differ." 
        ],
        'elabs': [
            "The gating network outputs expert weights.",
            "Top-k routing sends each token to a fixed small number of experts.",
            "Load imbalance across experts is a key challenge in MoE training.",
            "Switch Transformers route each token to only one expert.",
            "Routing decisions use similarity of token embeddings.",
            "During inference, only a subset of experts are activated.",
            "Expert dropout regularizes the gating network.",
            "Load balancing loss encourages an even distribution of tokens.",
            "Token dropping removes tokens with low gating scores.",
            "Experts share architecture but maintain separate weights." ]
    },
    'pytorch resource accounting': {
        'hints': [
            "It doesn't include unused cached memory.",
            "Useful after large tensors are deleted.",
            "It keeps track of dynamic loss scaling.",
            "Gradients aren't needed for inference.",
            "There is an API returning the high watermark.",
            "It times kernels to find the fastest convolution.",
            "They reduce communication overhead.",
            "Shows memory the allocator reserved from the driver.",
            "It records operation traces.",
            "They annotate events on the timeline." 
        ],
        'elabs': [
            "torch.cuda.memory_allocated() reports memory managed by PyTorch's allocator.",
            "torch.cuda.empty_cache frees unused GPU memory without exiting.",
            "The grad scaler consumes extra memory in mixed precision training.",
            "torch.no_grad() saves memory by not storing gradients during eval.",
            "torch.cuda.max_memory_allocated tracks peak memory usage.",
            "torch.backends.cudnn.benchmark=True finds optimal convolution algorithms.",
            "Gradient buckets fuse gradients before all-reduce in DDP.",
            "torch.cuda.memory_reserved() shows total reserved memory including cache.",
            "torch.autograd.profiler helps identify time and memory hotspots.",
            "NVTX ranges create colorful traces for profiling tools." ]
    },
    'evaluation': {
        'hints': [
            "Lower is better for predicting the sample.",
            "They compare generated text to references.",
            "It's a broad benchmark, not just one task.",
            "Automated scores don't capture everything.",
            "Testing generalization without specific training.",
            "Do confidence scores match reality?",
            "They include many subject-area questions.",
            "It's based on recall of n-grams.",
            "Run two options and see which users prefer.",
            "They assess harmful content." 
        ],
        'elabs': [
            "Perplexity measures the likelihood of test data under the model.",
            "BLEU and ROUGE evaluate machine translation and summarization quality.",
            "The HELM benchmark provides holistic evaluation across scenarios.",
            "Humans judge nuances that metrics miss.",
            "Zero-shot performance evaluates tasks the model wasn't fine-tuned for.",
            "Model calibration checks that probabilities match true outcomes.",
            "MMLU tests general knowledge and reasoning ability.",
            "ROUGE is a common metric for summarization tasks.",
            "A/B testing compares user engagement across model versions.",
            "Toxicity and bias scores are safety-focused metrics." ]
    }
}

for topic, info in updates.items():
    hints = info['hints']
    elabs = info['elabs']
    for q, h, e in zip(data[topic], hints, elabs):
        q['hint'] = h
        q['elaboration'] = e

json.dump(data, open('questions.json','w'), indent=4, ensure_ascii=False)
